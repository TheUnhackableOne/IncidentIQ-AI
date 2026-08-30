export interface Incident {
  id: string;
  description: string;
  service: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  status: 'investigating' | 'completed' | 'failed';
  created_at: string;
  updated_at: string;
}

export interface RootCauseHypothesis {
  hypothesis: string;
  confidence: number;
  supporting_evidence: string[];
  contradicting_evidence: string[];
  affected_service: string;
  recommended_verification: string;
}

export interface InvestigationReport {
  incident_id: string;
  summary: string;
  probable_root_cause: RootCauseHypothesis[];
  timeline: TimelineEvent[];
  severity: string;
  confidence: number;
  evidence: Evidence[];
  remediation: string[];
  unresolved_questions: string[];
  verification_steps: string[];
}

export interface TimelineEvent {
  timestamp: string;
  event: string;
  source: string;
}

export interface Evidence {
  evidence_id: string;
  source: string;
  source_type: string;
  excerpt: string;
  relevance_score: number;
  retrieval_method: string;
  metadata: Record<string, unknown>;
}

export interface EvaluationMetrics {
  recall_at_k: number;
  mrr: number;
  context_precision: number;
  context_recall: number;
  faithfulness: number;
  answer_relevance: number;
  evidence_accuracy: number;
  root_cause_accuracy: number;
  latency_ms: number;
  token_usage: TokenUsage;
}

export interface TokenUsage {
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
}
