import { NextRequest, NextResponse } from 'next/server';

const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8000';

export async function GET(
  request: NextRequest,
  { params }: { params: { domain: string } }
) {
  try {
    const { domain } = params;

    // Forward to Python backend
    const response = await fetch(`${PYTHON_API_URL}/api/samples/${domain}`);

    if (!response.ok) {
      throw new Error('Sample not found');
    }

    // Get the file blob
    const blob = await response.blob();
    const filename = response.headers.get('Content-Disposition')?.split('filename=')[1] || `${domain}_sample.csv`;

    // Return as file download
    return new NextResponse(blob, {
      headers: {
        'Content-Type': 'text/csv',
        'Content-Disposition': `attachment; filename=${filename}`,
      },
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Sample download failed' },
      { status: 404 }
    );
  }
}
