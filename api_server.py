"""
FastAPI server for ERP Intelligence Agent backend.
Provides REST API endpoints for the Next.js frontend.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import pandas as pd
import io
import os
from pathlib import Path

from agent_modules.orchestrator import ERPAgentOrchestrator
from data_loader.loader import DataLoader
from data_loader.schema_detector import SchemaDetector
from models.base import DataType

app = FastAPI(title="ERP Intelligence API", version="1.0.0")

# CORS configuration for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class AnalyzeRequest(BaseModel):
    files: List[Dict[str, Any]]
    config: Dict[str, Any]

class FileUploadResponse(BaseModel):
    success: bool
    file_id: str
    file_name: str
    data_type: str
    rows: int
    columns: List[str]
    schema_confidence: float
    required_columns_present: bool
    quality_issues: List[Dict[str, Any]]

# Global storage for uploaded files (in production, use database)
uploaded_files_storage: Dict[str, pd.DataFrame] = {}
file_metadata: Dict[str, Dict[str, Any]] = {}


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "ERP Intelligence API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)) -> FileUploadResponse:
    """
    Upload and validate a single data file.
    Returns schema match and data quality assessment.
    """
    try:
        # Read file content
        content = await file.read()

        # Load into DataFrame
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Use CSV or Excel.")

        # Detect schema and data type
        schema_detector = SchemaDetector()
        detected_type, confidence = schema_detector.detect_with_confidence(df)

        # Validate schema match
        schema_match = schema_detector.create_schema_match(df, detected_type)

        # Get required fields
        required_fields = schema_detector._get_required_fields(detected_type)
        matched_fields = [m.expected_field for m in schema_match.column_mappings]
        required_matched = [f for f in required_fields if f in matched_fields]
        required_columns_present = len(required_matched) / max(len(required_fields), 1) >= 0.5

        # Load data through DataLoader for quality check
        loader = DataLoader()
        temp_file = f"temp_{file.filename}"
        df.to_csv(temp_file, index=False)
        loader.load_file(temp_file)
        os.remove(temp_file)
        quality_report = loader.quality_report

        # Store file
        file_id = f"file_{len(uploaded_files_storage) + 1}"
        uploaded_files_storage[file_id] = df
        file_metadata[file_id] = {
            "name": file.filename,
            "type": detected_type.value,
            "rows": len(df),
            "columns": list(df.columns),
            "confidence": confidence,
            "required_present": required_columns_present
        }

        return FileUploadResponse(
            success=True,
            file_id=file_id,
            file_name=file.filename,
            data_type=detected_type.value,
            rows=len(df),
            columns=list(df.columns),
            schema_confidence=confidence,
            required_columns_present=required_columns_present,
            quality_issues=quality_report.issues if hasattr(quality_report, 'issues') else []
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing error: {str(e)}")


@app.post("/api/analyze")
async def analyze_data(request: AnalyzeRequest) -> Dict[str, Any]:
    """
    Analyze uploaded files based on configuration.
    ONLY runs analyzers for domains with valid uploaded data.
    """
    try:
        files = request.files
        config = request.config

        # Build data_frames dict ONLY for uploaded files
        data_frames = {}
        file_data_types = []

        for file_info in files:
            file_id = file_info.get('id')
            if file_id not in uploaded_files_storage:
                continue

            df = uploaded_files_storage[file_id]
            metadata = file_metadata.get(file_id, {})
            data_type = metadata.get('type', 'unknown')

            # CRITICAL: Only include if schema validation passed
            if not metadata.get('required_present', False):
                continue

            # CRITICAL: Only include if confidence is sufficient
            if metadata.get('confidence', 0) < 0.5:
                continue

            # Map to expected key
            data_frames[data_type] = df
            file_data_types.append(data_type)

        # If no valid files, return empty result
        if not data_frames:
            return {
                "success": False,
                "error": "No valid data files. Please ensure files have required columns.",
                "enabled_domains": [],
                "data_types": []
            }

        # Run multi-file analysis with ONLY enabled domains
        orchestrator = ERPAgentOrchestrator()
        analysis_level = config.get('analysis_depth', 'detailed').capitalize()
        results = orchestrator.analyze_multi_file(data_frames, analysis_level)

        # Return results with enabled_domains key
        return {
            "success": True,
            "data": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.get("/api/templates/{domain}")
async def download_template(domain: str):
    """
    Download template file for a specific domain.
    """
    template_dir = Path("templates")
    template_map = {
        "financial": "financial_template.xlsx",
        "manufacturing": "manufacturing_template.xlsx",
        "inventory": "inventory_template.xlsx",
        "sales": "sales_template.xlsx",
        "purchase": "purchase_template.xlsx"
    }

    template_file = template_map.get(domain.lower())
    if not template_file:
        raise HTTPException(status_code=404, detail="Template not found")

    file_path = template_dir / template_file

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Template file not found")

    return FileResponse(
        path=str(file_path),
        filename=template_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={template_file}"}
    )


@app.get("/api/samples/{domain}")
async def download_sample(domain: str):
    """
    Download sample data file for a specific domain.
    """
    sample_dir = Path("sample_data")
    sample_map = {
        "financial": "sample_financial.csv",
        "manufacturing": "sample_manufacturing.csv",
        "inventory": "sample_inventory.csv",
        "sales": "sample_sales.csv",
        "purchase": "sample_purchase.csv"
    }

    sample_file = sample_map.get(domain.lower())
    if not sample_file:
        raise HTTPException(status_code=404, detail="Sample not found")

    file_path = sample_dir / sample_file

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Sample file not found")

    return FileResponse(
        path=str(file_path),
        filename=sample_file,
        media_type="text/csv" if sample_file.endswith('.csv') else "application/vnd.ms-excel",
        headers={"Content-Disposition": f"attachment; filename={sample_file}"}
    )


@app.get("/api/health")
async def health_check():
    """Health check for monitoring."""
    return {
        "status": "healthy",
        "service": "ERP Intelligence API",
        "files_in_memory": len(uploaded_files_storage)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
