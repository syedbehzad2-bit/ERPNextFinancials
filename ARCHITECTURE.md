# ERP Intelligence Agent - Complete Architecture Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Directory Structure](#directory-structure)
5. [Frontend Architecture (Next.js)](#frontend-architecture-nextjs)
6. [Backend Architecture (Python)](#backend-architecture-python)
7. [Data Flow](#data-flow)
8. [Component Architecture](#component-architecture)
9. [State Management](#state-management)
10. [Theme System](#theme-system)
11. [API Integration](#api-integration)
12. [Database Schema](#database-schema)
13. [Deployment Architecture](#deployment-architecture)

---

## Overview

The ERP Intelligence Agent is a full-stack application that analyzes ERP data across 5 business domains (Financial, Manufacturing, Inventory, Sales, Purchase) and provides AI-powered insights, risk assessments, and actionable recommendations.

### Key Features
- **Multi-domain Analysis**: Analyzes financial, manufacturing, inventory, sales, and purchase data
- **AI-Powered Insights**: Uses OpenAI Agents SDK with Gemini 2.5 Flash
- **Interactive Visualizations**: 9+ Chart.js visualizations with theme support
- **Light/Dark Theme**: Professional 3D UI with smooth theme transitions
- **Cross-file Analysis**: Identifies relationships between different data domains
- **Risk Assessment**: 3-6 month forward-looking risk identification
- **Action Plans**: Prioritized recommendations with timelines

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                    (http://localhost:3000)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   NEXT.JS FRONTEND (Port 3000)                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  App Router Pages                                         │  │
│  │  - / (Upload)                                             │  │
│  │  - /analysis (Config)                                     │  │
│  │  - /results (Dashboard)                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Components                                               │  │
│  │  - UI (Button, Card, Tabs, Modal, ThemeToggle)           │  │
│  │  - Charts (9 Chart.js visualizations)                    │  │
│  │  - Layout (Sidebar, Header, Navigation)                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  State Management (Zustand)                              │  │
│  │  - uploadedFiles                                          │  │
│  │  - analysisConfig                                         │  │
│  │  - analysisResults                                        │  │
│  │  - theme (light/dark)                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ REST API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               NEXT.JS API ROUTES (Port 3000/api)                 │
│  - POST /api/upload       - File upload handler                 │
│  - POST /api/analyze      - Analysis orchestration              │
│  - GET  /api/results      - Results retrieval                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Internal Call / HTTP
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PYTHON BACKEND (Port 8000)                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Data Loader                                              │  │
│  │  - Schema Detection                                       │  │
│  │  - Data Validation                                        │  │
│  │  - Data Cleaning                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Domain Analyzers                                         │  │
│  │  - FinancialAnalyzer (P&L, margins, expenses)            │  │
│  │  - ManufacturingAnalyzer (efficiency, wastage)           │  │
│  │  - InventoryAnalyzer (aging, turnover, dead stock)       │  │
│  │  - SalesAnalyzer (trends, concentration, products)       │  │
│  │  - PurchaseAnalyzer (suppliers, lead times)              │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  AI Orchestrator (OpenAI Agents SDK)                     │  │
│  │  - 6 Specialized Agents                                   │  │
│  │  - Tool-based architecture                                │  │
│  │  - Gemini 2.5 Flash API                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Engines                                                  │  │
│  │  - Insight Engine (finding + impact + action)            │  │
│  │  - Recommendation Engine (prioritized actions)           │  │
│  │  - Risk Engine (3-6 month forward risks)                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ API Call
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              GEMINI 2.5 FLASH API (Google Cloud)                 │
│  - Model: gemini-2.5-flash                                       │
│  - Temperature: 0.1 (deterministic)                              │
│  - Max Tokens: 4000                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 14.2.5 | React framework with App Router |
| **React** | 18 | UI library |
| **TypeScript** | 5+ | Type safety |
| **Tailwind CSS** | 3.4.7 | Utility-first CSS framework |
| **Chart.js** | 4.4.3 | Interactive charts |
| **react-chartjs-2** | 5.2.0 | React wrapper for Chart.js |
| **Zustand** | 4.5.4 | State management |
| **Lucide React** | 0.400.0 | Icon library |
| **clsx** | 2.1.1 | Conditional class names |
| **tailwind-merge** | 2.3.0 | Merge Tailwind classes |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.9+ | Backend language |
| **Streamlit** | Latest | Original UI (legacy) |
| **Pydantic** | 2.x | Data validation |
| **Pandas** | Latest | Data manipulation |
| **OpenAI Agents SDK** | Latest | AI agent orchestration |
| **Gemini API** | 2.5 Flash | LLM for insights |

### Development Tools
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Git** - Version control
- **npm** - Package management

---

## Directory Structure

```
D:\ERP Agent\
│
├── next-app/                          # Next.js Frontend
│   ├── src/
│   │   ├── app/                       # App Router pages
│   │   │   ├── layout.tsx             # Root layout with ThemeProvider
│   │   │   ├── page.tsx               # Upload page (/)
│   │   │   ├── globals.css            # Global styles + 3D effects
│   │   │   ├── analysis/
│   │   │   │   └── page.tsx           # Analysis config page
│   │   │   ├── results/
│   │   │   │   └── page.tsx           # Results dashboard page
│   │   │   └── api/                   # API routes
│   │   │       └── analyze/
│   │   │           └── route.ts       # POST /api/analyze
│   │   │
│   │   ├── components/
│   │   │   ├── ui/                    # Base UI components
│   │   │   │   ├── Button.tsx         # 3D button with variants
│   │   │   │   ├── Card.tsx           # 3D card with elevation
│   │   │   │   ├── Modal.tsx          # Modal dialog
│   │   │   │   ├── Tabs.tsx           # Tab navigation
│   │   │   │   ├── ThemeToggle.tsx    # Sun/Moon theme toggle
│   │   │   │   └── index.ts           # Exports
│   │   │   │
│   │   │   ├── charts/                # Chart.js visualizations
│   │   │   │   ├── chartConfig.ts     # Theme-aware chart configs
│   │   │   │   ├── RevenueChart.tsx   # Line chart
│   │   │   │   ├── MarginChart.tsx    # Line chart with threshold
│   │   │   │   ├── AgingChart.tsx     # Donut chart
│   │   │   │   ├── ParetoChart.tsx    # Bar + Line (80/20)
│   │   │   │   ├── EfficiencyChart.tsx # Color-coded bars
│   │   │   │   ├── WastageChart.tsx   # Horizontal bars
│   │   │   │   ├── DeliveryChart.tsx  # Donut chart
│   │   │   │   ├── SpendChart.tsx     # Horizontal bars
│   │   │   │   ├── LeadTimeChart.tsx  # Line chart
│   │   │   │   └── index.ts           # Exports
│   │   │   │
│   │   │   ├── layout/                # Layout components
│   │   │   │   ├── Sidebar.tsx        # Fixed sidebar navigation
│   │   │   │   ├── Header.tsx         # Top header with search
│   │   │   │   ├── SidebarNav.tsx     # Navigation items
│   │   │   │   └── index.ts           # Exports
│   │   │   │
│   │   │   └── theme/
│   │   │       └── ThemeProvider.tsx  # React Context for theme
│   │   │
│   │   ├── lib/
│   │   │   ├── types.ts               # TypeScript type definitions
│   │   │   ├── formatters.ts          # Number/currency formatters
│   │   │   └── constants.ts           # App constants
│   │   │
│   │   └── store/
│   │       └── useAppStore.ts         # Zustand store
│   │
│   ├── public/                        # Static assets
│   ├── .next/                         # Build output (gitignored)
│   ├── node_modules/                  # Dependencies (gitignored)
│   ├── package.json                   # Dependencies manifest
│   ├── tsconfig.json                  # TypeScript config
│   ├── tailwind.config.ts             # Tailwind config
│   ├── postcss.config.js              # PostCSS config
│   ├── next.config.js                 # Next.js config
│   └── README.md                      # Frontend documentation
│
├── ui/                                # Streamlit UI (Legacy)
│   ├── pages/
│   │   ├── upload_page.py
│   │   ├── analysis_page.py
│   │   └── results_page.py
│   ├── components/
│   │   ├── charts.py                  # Plotly charts
│   │   └── results_display.py
│   └── styles.py
│
├── models/                            # Pydantic Data Models
│   ├── base.py                        # Enums (DataType, Severity, Priority)
│   ├── analysis_output.py             # Insight, Recommendation, Risk
│   ├── financial.py                   # PLStatement, ExpenseItem
│   ├── manufacturing.py               # Production, Wastage
│   ├── inventory.py                   # Stock, Aging
│   ├── sales.py                       # Order, Customer
│   └── purchase.py                    # PurchaseOrder, Supplier
│
├── analyzers/                         # Domain Analysis Logic
│   ├── base_analyzer.py               # Abstract base class
│   ├── financial_analyzer.py          # Financial KPIs & analysis
│   ├── manufacturing_analyzer.py      # Production analysis
│   ├── inventory_analyzer.py          # Stock analysis
│   ├── sales_analyzer.py              # Sales trends & patterns
│   └── purchase_analyzer.py           # Supplier analysis
│
├── engines/                           # Intelligence Engines
│   ├── insight_engine.py              # Transforms analysis to insights
│   ├── recommendation_engine.py       # Generates action plans
│   └── risk_engine.py                 # Identifies forward risks
│
├── agent_modules/                     # AI Agent System
│   ├── orchestrator.py                # Main agent orchestrator
│   └── tools.py                       # Agent tools
│
├── data_loader/                       # Data Processing
│   ├── loader.py                      # DataLoader class
│   ├── schema_detector.py             # Auto-detects data type
│   ├── validators.py                  # Data validation
│   └── cleaners.py                    # Data cleaning
│
├── config/                            # Configuration
│   ├── settings.py                    # App settings, API keys
│   └── prompts.py                     # AI agent prompts
│
├── tests/                             # Unit tests
│   ├── test_data_loader.py
│   ├── test_analyzers.py
│   └── fixtures/
│
├── sample_data/                       # Sample CSV/Excel files
├── templates/                         # Excel templates for users
├── app.py                             # Streamlit entry point (legacy)
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
```

---

## Frontend Architecture (Next.js)

### 1. App Router Structure

```typescript
// Page hierarchy
/                    → Upload page (src/app/page.tsx)
/analysis            → Analysis config (src/app/analysis/page.tsx)
/results             → Results dashboard (src/app/results/page.tsx)
/api/analyze         → Analysis API (src/app/api/analyze/route.ts)
```

### 2. Component Hierarchy

```
RootLayout (layout.tsx)
├── ThemeProvider
    └── Body
        ├── Sidebar
        │   ├── Logo
        │   ├── SidebarNav
        │   │   └── Navigation Items
        │   └── Status Panel
        │
        └── Main Content
            ├── Header
            │   ├── Search
            │   ├── Notifications
            │   ├── ThemeToggle
            │   └── User Menu
            │
            └── Page Content
                ├── Upload Page
                │   ├── Dropzone
                │   ├── File List
                │   └── Templates Sidebar
                │
                ├── Analysis Page
                │   ├── File Summary
                │   ├── Config Options
                │   └── Run Button
                │
                └── Results Page
                    ├── Executive Summary
                    ├── KPI Cards
                    ├── Chart Tabs
                    ├── Insights (tabbed)
                    ├── Risks Assessment
                    └── Action Plan
```

### 3. State Flow

```typescript
// Zustand Store Structure
interface AppState {
  // Theme
  theme: 'light' | 'dark'

  // Files
  uploadedFiles: UploadedFile[]

  // Analysis
  analysisConfig: AnalysisConfig
  analysisResults: AnalysisResults | null
  isAnalyzing: boolean

  // Actions
  setTheme: (theme: Theme) => void
  toggleTheme: () => void
  addFile: (file: UploadedFile) => void
  removeFile: (fileId: string) => void
  setAnalysisConfig: (config: AnalysisConfig) => void
  setAnalysisResults: (results: AnalysisResults | null) => void
  setIsAnalyzing: (isAnalyzing: boolean) => void
}
```

### 4. Routing & Navigation

```
User uploads files → (/) Upload Page
        ↓
Click "Configure Analysis"
        ↓
(/analysis) Analysis Page
        ↓
Click "Run Analysis" → API call to /api/analyze
        ↓
Navigate to (/results) Results Page
        ↓
View insights, charts, risks, actions
```

---

## Backend Architecture (Python)

### 1. Data Processing Pipeline

```python
# Step 1: Data Upload
User uploads CSV/Excel → Frontend

# Step 2: Data Loading
DataLoader.load_file(file)
    ├── SchemaDetector.detect_type(df)      # Auto-detect: financial, inventory, etc.
    ├── Validator.validate(df, data_type)  # Check required columns
    └── Cleaner.clean(df)                   # Standardize formats

# Step 3: Data Quality Check
DataQualityReport
    ├── Missing values analysis
    ├── Duplicate detection
    ├── Column validation
    └── Usability flag

# Step 4: Domain Analysis
BaseAnalyzer.analyze(df)
    ├── calculate_kpis()                    # Domain-specific KPIs
    ├── trend_analysis()                    # Time series patterns
    ├── variance_analysis()                 # Planned vs actual
    ├── pareto_analysis()                   # 80/20 rule
    └── ratio_analysis()                    # Financial ratios

# Step 5: AI Orchestration
Orchestrator.run_analysis(data, config)
    ├── Load specialized agents
    ├── Execute domain analyses
    ├── Generate insights (InsightEngine)
    ├── Create recommendations (RecommendationEngine)
    ├── Identify risks (RiskEngine)
    └── Synthesize ExecutiveReport

# Step 6: Results Generation
ExecutiveReport
    ├── executive_summary: List[str]
    ├── financial_insights: List[Insight]
    ├── manufacturing_insights: List[Insight]
    ├── inventory_insights: List[Insight]
    ├── sales_insights: List[Insight]
    ├── critical_risks: List[Risk]
    └── action_plan: List[Recommendation]
```

### 2. Analyzer Architecture

```python
# Base Analyzer (Abstract)
class BaseAnalyzer(ABC):
    @abstractmethod
    def calculate_kpis(self, df: pd.DataFrame) -> Dict

    @abstractmethod
    def analyze(self, df: pd.DataFrame) -> AnalysisResult

    # Shared analysis methods
    def trend_analysis(self, df, value_col, date_col)
    def variance_analysis(self, df, actual_col, planned_col)
    def pareto_analysis(self, df, category_col, value_col)
    def ratio_analysis(self, df, numerator_col, denominator_col)

# Domain Analyzers extend BaseAnalyzer
FinancialAnalyzer → Margins, Revenue, Expenses
ManufacturingAnalyzer → Efficiency, Wastage, Cost per Unit
InventoryAnalyzer → Aging, Dead Stock, Turnover
SalesAnalyzer → Trends, Product Performance, Concentration
PurchaseAnalyzer → Suppliers, Lead Times, Delivery
```

### 3. AI Agent System

```python
# Agent Architecture (OpenAI Agents SDK)
Orchestrator
    ├── Financial Analyst Agent
    │   ├── Tools: analyze_financials, calculate_ratios
    │   └── Prompt: "Analyze P&L, margins, expenses"
    │
    ├── Manufacturing Analyst Agent
    │   ├── Tools: analyze_manufacturing, calculate_efficiency
    │   └── Prompt: "Analyze production, wastage"
    │
    ├── Inventory Analyst Agent
    │   ├── Tools: analyze_inventory, identify_dead_stock
    │   └── Prompt: "Analyze stock aging, turnover"
    │
    ├── Sales Analyst Agent
    │   ├── Tools: analyze_sales, calculate_trends
    │   └── Prompt: "Analyze trends, products, concentration"
    │
    ├── Purchase Analyst Agent
    │   ├── Tools: analyze_purchases, supplier_performance
    │   └── Prompt: "Analyze suppliers, lead times"
    │
    └── Executive Advisor Agent
        ├── Tools: synthesize_insights, identify_risks
        └── Prompt: "Create executive summary, prioritize actions"

# Tool Execution Flow
Agent → Selects Tool → Executes Analyzer → Returns Results → LLM Processes → Generates Insight
```

---

## Data Flow

### Complete User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USER UPLOADS FILES                                            │
│    - Upload CSV/Excel files                                      │
│    - Drag & drop or file browser                                 │
│    - Multiple files supported                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. FILE PROCESSING (Frontend)                                    │
│    - File validation (size, format)                              │
│    - Add to Zustand store                                        │
│    - Display file metadata                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. ANALYSIS CONFIGURATION                                        │
│    - Select analysis types (financial, inventory, etc.)          │
│    - Choose depth (summary/detailed/comprehensive)               │
│    - Enable/disable cross-file analysis                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. TRIGGER ANALYSIS                                              │
│    - POST /api/analyze                                           │
│    - Send files + config                                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. BACKEND PROCESSING                                            │
│    a. Data Loading                                               │
│       - Parse CSV/Excel                                          │
│       - Detect data type (schema detection)                      │
│       - Validate columns                                         │
│       - Clean data                                               │
│                                                                  │
│    b. Data Quality Assessment                                    │
│       - Check missing values                                     │
│       - Detect duplicates                                        │
│       - Flag issues                                              │
│                                                                  │
│    c. Domain Analysis                                            │
│       - Run appropriate analyzer                                 │
│       - Calculate KPIs                                           │
│       - Perform trend analysis                                   │
│       - Identify patterns                                        │
│                                                                  │
│    d. AI Orchestration                                           │
│       - Initialize agents                                        │
│       - Execute tools                                            │
│       - Call Gemini API                                          │
│       - Generate insights                                        │
│                                                                  │
│    e. Insight Generation                                         │
│       - Transform analysis to insights                           │
│       - Format: Finding + Impact + Action                        │
│       - Categorize by severity                                   │
│                                                                  │
│    f. Recommendation Creation                                    │
│       - Generate action plans                                    │
│       - Prioritize by timeline                                   │
│       - Estimate impact                                          │
│                                                                  │
│    g. Risk Identification                                        │
│       - 3-6 month forward risks                                  │
│       - Probability assessment                                   │
│       - Financial impact                                         │
│       - Mitigation strategies                                    │
│                                                                  │
│    h. Executive Report Synthesis                                 │
│       - Create 5-7 bullet summary                                │
│       - Aggregate all insights                                   │
│       - Compile risks and actions                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. RETURN RESULTS                                                │
│    - ExecutiveReport JSON                                        │
│    - Store in Zustand                                            │
│    - Navigate to /results                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. RESULTS DISPLAY                                               │
│    - Executive Summary (5-7 points)                              │
│    - KPI Cards (dynamic by domain)                               │
│    - Charts (9 visualizations)                                   │
│    - Insights (tabbed by domain)                                 │
│    - Risks (critical/high/medium/low)                            │
│    - Action Plan (prioritized by timeline)                       │
│    - Export options (JSON/Text)                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### UI Components

#### 1. Button Component
```typescript
// 3D Button with variants
<Button
  variant="primary" | "secondary" | "success" | "warning" | "error"
  size="sm" | "md" | "lg"
  is3D={true}
  loading={false}
>
  Click Me
</Button>

// CSS Implementation
.btn-3d {
  box-shadow: 0 4px 0 var(--primary-hover), 0 5px 10px rgba(0,0,0,0.2);
}
.btn-3d:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 0 var(--primary-hover), 0 8px 15px rgba(0,0,0,0.25);
}
```

#### 2. Card Component
```typescript
// 3D Card with elevation
<Card
  variant="default" | "elevated" | "bordered"
  padding="none" | "sm" | "md" | "lg"
>
  <CardHeader title="Title" subtitle="Subtitle" />
  Content here
</Card>

// CSS Implementation
.card-3d {
  background: linear-gradient(145deg, var(--surface), var(--surface));
  box-shadow: 5px 5px 10px var(--shadow-color),
              -5px -5px 10px rgba(255,255,255,0.8);
}
```

#### 3. Chart Components
```typescript
// Revenue Chart (Line + Area)
<RevenueChart
  data={[
    { period: 'Jan', revenue: 180000 },
    { period: 'Feb', revenue: 195000 }
  ]}
/>

// All 9 Charts:
RevenueChart      → Line with area fill
MarginChart       → Line with threshold line
AgingChart        → Donut pie
ParetoChart       → Bar + Cumulative line
EfficiencyChart   → Color-coded bars
WastageChart      → Horizontal bars
DeliveryChart     → Donut pie
SpendChart        → Horizontal bars
LeadTimeChart     → Line with markers
```

### Layout Components

#### 1. Sidebar
```typescript
// Fixed sidebar with navigation
<Sidebar>
  - Logo
  - Navigation (Upload, Analysis, Results)
  - Status (Files loaded, Analyzed)
  - Version
</Sidebar>

// Features:
- Fixed position (left: 0)
- 256px width (w-64)
- Dark gradient background
- Active state indicators
```

#### 2. Header
```typescript
// Top header bar
<Header>
  - Search input
  - Notification bell
  - Theme toggle
  - User menu
</Header>

// Features:
- Sticky position
- Glass morphism effect
- Responsive search
```

---

## State Management

### Zustand Store

```typescript
// Store Structure
{
  // Theme State
  theme: 'light' | 'dark'

  // File State
  uploadedFiles: [
    {
      id: string
      name: string
      type: DataType
      size: number
      rows: number
      columns: string[]
      uploadedAt: string
    }
  ]

  // Analysis State
  analysisConfig: {
    analysis_types: {
      financial: boolean
      manufacturing: boolean
      inventory: boolean
      sales: boolean
      purchase: boolean
    }
    analysis_depth: 'summary' | 'detailed' | 'comprehensive'
    enable_cross_file_analysis: boolean
  }

  analysisResults: {
    generated_at: string
    data_source: string
    data_types: DataType[]
    executive_summary: string[]

    financial: DomainResults
    manufacturing: DomainResults
    inventory: DomainResults
    sales: DomainResults
    purchase: DomainResults

    critical_risks: Risk[]
    action_plan: Recommendation[]
  } | null

  isAnalyzing: boolean
}

// Persistence
- localStorage key: 'erp-agent-storage'
- Partialize: theme, uploadedFiles, analysisConfig
- Hydration on mount
```

---

## Theme System

### 1. Color Variables

```css
/* Light Theme */
:root {
  --bg-primary: #f8fafc;
  --bg-secondary: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border-color: #e2e8f0;
  --primary: #6366f1;
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
}

/* Dark Theme */
.dark {
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --border-color: #334155;
  --primary: #818cf8;
  --success: #34d399;
  --warning: #fbbf24;
  --error: #f87171;
}
```

### 2. Theme Provider

```typescript
// React Context Provider
<ThemeProvider>
  {children}
</ThemeProvider>

// Features:
- localStorage persistence
- System preference detection
- Smooth transitions (200ms)
- Context-based hook (useTheme)
- Prevents flash of wrong theme
```

### 3. Theme Toggle

```typescript
// Toggle Button
<ThemeToggle />

// Behavior:
- Click to toggle light/dark
- Animated icon transition
- Updates document.documentElement.classList
- Persists to localStorage
```

---

## API Integration

### 1. Frontend → Next.js API

```typescript
// POST /api/analyze
async function analyzeFiles() {
  const response = await fetch('/api/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      files: uploadedFiles,
      config: analysisConfig
    })
  });

  const result = await response.json();
  return result.data; // AnalysisResults
}
```

### 2. Next.js API → Python Backend

```typescript
// app/api/analyze/route.ts
export async function POST(request: NextRequest) {
  const { files, config } = await request.json();

  // Call Python backend
  const response = await fetch('http://localhost:8000/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ files, config })
  });

  const results = await response.json();
  return NextResponse.json({ success: true, data: results });
}
```

### 3. Python Backend → Gemini API

```python
# agent_modules/orchestrator.py
from openai import OpenAI

client = OpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ],
    temperature=0.1,
    max_tokens=4000
)
```

---

## Database Schema

### Current: In-Memory (Zustand + localStorage)

No database currently - all state in browser localStorage.

### Future: PostgreSQL Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Files table
CREATE TABLE uploaded_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    file_name VARCHAR(255),
    file_type VARCHAR(50),
    data_type VARCHAR(50),
    rows INTEGER,
    columns JSONB,
    file_path TEXT,
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Analysis runs table
CREATE TABLE analysis_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    file_ids UUID[],
    config JSONB,
    status VARCHAR(50),
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Results table
CREATE TABLE analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_run_id UUID REFERENCES analysis_runs(id),
    executive_summary JSONB,
    insights JSONB,
    risks JSONB,
    recommendations JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Deployment Architecture

### Development

```
Local Machine
├── Frontend: http://localhost:3000 (Next.js dev server)
└── Backend: http://localhost:8000 (Python/FastAPI)
```

### Production (Recommended)

```
┌─────────────────────────────────────────────────────────────────┐
│                         VERCEL / NETLIFY                         │
│                    (Next.js Frontend Hosting)                    │
│                     https://erp-agent.vercel.app                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ API Calls
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RAILWAY / RENDER                            │
│                   (Python Backend Hosting)                       │
│                https://erp-agent-api.railway.app                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ API Calls
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       GOOGLE CLOUD                               │
│                     (Gemini 2.5 Flash API)                       │
└─────────────────────────────────────────────────────────────────┘
```

### Docker Deployment

```dockerfile
# Frontend Dockerfile (next-app/Dockerfile)
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]

# Backend Dockerfile (Dockerfile)
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build: ./next-app
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
```

---

## Performance Considerations

### Frontend Optimization
1. **Code Splitting**: Next.js automatic code splitting
2. **Image Optimization**: Next/Image for optimized images
3. **Lazy Loading**: Dynamic imports for charts
4. **Caching**: SWR or React Query for API caching
5. **Bundle Analysis**: next-bundle-analyzer

### Backend Optimization
1. **Async Processing**: Celery for background tasks
2. **Caching**: Redis for analysis results
3. **Database Indexing**: Indexes on frequently queried columns
4. **Connection Pooling**: SQLAlchemy connection pool
5. **Rate Limiting**: API rate limiting with slowapi

---

## Security Considerations

1. **API Keys**: Environment variables, never committed
2. **Input Validation**: Pydantic for backend, Zod for frontend
3. **File Upload**: Size limits, format validation, virus scanning
4. **CORS**: Configured for specific origins
5. **Authentication**: JWT tokens (future implementation)
6. **HTTPS**: TLS/SSL in production
7. **CSP**: Content Security Policy headers

---

## Testing Strategy

### Frontend Tests
```typescript
// Component tests (Jest + React Testing Library)
describe('Button', () => {
  it('renders with 3D styling', () => {
    render(<Button is3D>Click</Button>);
    expect(screen.getByText('Click')).toHaveClass('btn-3d');
  });
});

// E2E tests (Playwright)
test('upload and analyze flow', async ({ page }) => {
  await page.goto('/');
  await page.setInputFiles('input[type="file"]', 'sample.csv');
  await page.click('text=Run Analysis');
  await expect(page).toHaveURL('/results');
});
```

### Backend Tests
```python
# Unit tests (pytest)
def test_financial_analyzer():
    analyzer = FinancialAnalyzer()
    result = analyzer.calculate_kpis(sample_df)
    assert 'total_revenue' in result
    assert result['total_revenue'] > 0

# Integration tests
def test_full_analysis_pipeline():
    files = [test_financial_file]
    config = AnalysisConfig(...)
    result = orchestrator.run_analysis(files, config)
    assert len(result.executive_summary) >= 5
```

---

## Monitoring & Logging

### Frontend
- **Error Tracking**: Sentry
- **Analytics**: Google Analytics / Plausible
- **Performance**: Web Vitals monitoring

### Backend
- **Logging**: Python logging module + structured logs
- **Error Tracking**: Sentry
- **Performance**: APM (Application Performance Monitoring)
- **Metrics**: Prometheus + Grafana

---

## Future Enhancements

1. **Authentication & Authorization**
   - User accounts
   - Role-based access control
   - Multi-tenancy

2. **Database Integration**
   - PostgreSQL for data persistence
   - Historical analysis tracking
   - Collaborative features

3. **Real-time Updates**
   - WebSocket connections
   - Live progress tracking
   - Collaborative editing

4. **Advanced Analytics**
   - Machine learning predictions
   - Anomaly detection
   - Forecasting models

5. **Export Options**
   - PDF reports
   - Excel exports
   - PowerPoint presentations

6. **Integrations**
   - ERP system connectors
   - Google Sheets integration
   - API for third-party tools

---

## Conclusion

This architecture provides a modern, scalable foundation for the ERP Intelligence Agent with:
- Clean separation of concerns
- Type-safe frontend and backend
- AI-powered insights
- Professional UI/UX
- Easy deployment and scaling
- Room for future enhancements

For questions or contributions, refer to the README.md in the repository.
