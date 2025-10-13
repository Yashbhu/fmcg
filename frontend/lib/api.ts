export interface AnalysisResponse {
  status: string;
  message: string;
  technical_count?: number;
  pricing_count?: number;
  technical_analysis?: Array<{
    requirement_id: string;
    requirement_text: string;
    compliance_status: string;
    evidence: string;
    gaps: string;
    risk_level: string;
  }>;
  pricing_analysis?: Array<{
    item_id: string;
    item_description: string;
    baseline_price: number;
    proposal_price: number;
    variance: number;
    variance_percent: number;
    justification: string;
  }>;
}

export async function runAnalysis(): Promise<AnalysisResponse> {
  const response = await fetch('http://127.0.0.1:8000/analyze/run', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Analysis failed');
  }

  return response.json();
}
