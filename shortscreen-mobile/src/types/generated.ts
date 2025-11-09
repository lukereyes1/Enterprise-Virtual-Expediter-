/**
 * AUTO-GENERATED TypeScript types from Python Pydantic models
 * DO NOT EDIT MANUALLY - Run scripts/gen_typescript_types.py to regenerate
 */


/**
 * Statistical distribution of a factor score.
 */
export interface FactorDistribution {
  /** Factor name */
  factor: string;
  /** Mean score */
  mean: number;
  /** Median score */
  median: number;
  /** Standard deviation */
  std: number;
  /** Minimum score */
  min: number;
  /** Maximum score */
  max: number;
  /** 25th percentile */
  p25: number;
  /** 75th percentile */
  p75: number;
}

/**
 * Metrics for a single phase of job execution.
 */
export interface JobPhaseMetrics {
  /** Name of the execution phase */
  phase_name: string;
  /** Duration of the phase in seconds */
  duration_seconds: number;
  /** Number of records processed */
  records_processed: number;
  /** Whether the phase succeeded */
  success: boolean;
  /** Error message if phase failed */
  error?: string | null;
}

/**
 * Status of a job execution.
 */
export type JobStatus = "success" | "partial" | "failed" | "running" | "pending";

/**
 * Types of jobs in the screening service.
 */
export type JobType = "full_refresh_daily" | "incremental_intraday" | "on_demand_scan";

/**
 * Macro regime indicators.

Each indicator is a value between 0 and 1, where higher values
indicate stronger conditions for that regime.
 */
export interface MacroRegime {
  /** Economic downturn risk (0-1) */
  downturn: number;
  /** Inflation pressure (0-1) */
  inflation: number;
  /** Liquidity stress (0-1) */
  liquidity: number;
}

/**
 * Narrative summary of screening results.
 */
export interface NarrativeSummary {
  /** One-line summary */
  headline: string;
  /** Bullet points of key findings */
  key_findings: Array<string>;
  /** Overall risk assessment paragraph */
  risk_assessment: string;
  /** Sector-specific insights */
  sector_insights: string;
  /** Recommended actions */
  recommendations: Array<string>;
}

/**
 * Metadata for a screening report.
 */
export interface ReportMetadata {
  /** Unique report identifier */
  report_id: string;
  /** Report generation timestamp */
  timestamp: string;
  /** Macro regime used for screening */
  regime: MacroRegime;
  /** Total universe size */
  universe_size: number;
  /** Number of candidates generated */
  candidates_count: number;
  /** Execution time in seconds */
  execution_time_seconds: number;
}

/**
 * Risk indicator scores.
 */
export interface RiskIndicators {
  /** Overall market risk-off sentiment (0-100) */
  risk_off_score: number;
  /** Small cap stress level (0-100) */
  small_cap_stress_score: number;
  /** Leverage stress across universe (0-100) */
  leverage_stress_score: number;
  /** Valuation extremes indicator (0-100) */
  valuation_extremes_score: number;
}

/**
 * Distribution of candidates by sector.
 */
export interface SectorDistribution {
  /** Sector name */
  sector: string;
  /** Number of candidates in sector */
  count: number;
  /** Percentage of total */
  percentage: number;
  /** Average vulnerability score */
  avg_score: number;
}

/**
 * A short candidate with all relevant scores and metadata.
 */
export interface ShortCandidate {
  /** Stock ticker symbol */
  ticker: string;
  /** Overall vulnerability score (0-100) */
  global_vulnerability_score: number;
  /** Theme with highest score */
  dominant_theme: string;
  /** Score for dominant theme */
  dominant_theme_score: number;
  /** Scores for all themes */
  theme_scores: Record<string, number>;
  /** Valuation factor score */
  valuation_score: number;
  /** Profitability factor score */
  profitability_score: number;
  /** Growth factor score */
  growth_score: number;
  /** Leverage factor score */
  leverage_score: number;
  /** Quality factor score */
  quality_score: number;
  /** Market factor score */
  market_score: number;
  /** Market cap in millions */
  market_cap: number;
  /** Sector classification */
  sector: string;
  /** Revenue growth rate */
  revenue_growth: number;
  /** Net profit margin */
  net_margin: number;
  /** Debt-to-Equity ratio */
  debt_to_equity: number;
  /** Market beta */
  beta: number;
}

/**
 * Distribution of candidates by dominant theme.
 */
export interface ThemeDistribution {
  /** Theme name */
  theme: string;
  /** Number of candidates with this dominant theme */
  count: number;
  /** Percentage of total */
  percentage: number;
  /** Average theme score */
  avg_score: number;
}

/**
 * Percentile-based factor scores for a ticker.

Each score is a percentile rank (0-100) where higher values indicate
more bearish characteristics for that factor.
 */
export interface FactorScores {
  /** Stock ticker symbol */
  ticker: string;
  /** Valuation score (higher = more expensive = more bearish) */
  valuation_score: number;
  /** Profitability score (higher = less profitable = more bearish) */
  profitability_score: number;
  /** Growth score (higher = negative/slowing growth = more bearish) */
  growth_score: number;
  /** Leverage score (higher = more levered = more bearish) */
  leverage_score: number;
  /** Quality score (higher = lower quality = more bearish) */
  quality_score: number;
  /** Market score (higher = higher beta/momentum issues = more bearish) */
  market_score: number;
}

/**
 * Fundamental data for a ticker.
 */
export interface FundamentalData {
  /** Stock ticker symbol */
  ticker: string;
  /** Total revenue in millions */
  revenue: number;
  /** Year-over-year revenue growth rate */
  revenue_growth: number;
  /** EBITDA in millions */
  ebitda: number;
  /** Net income in millions */
  net_income: number;
  /** Free cash flow in millions */
  free_cash_flow: number;
  /** Total debt in millions */
  total_debt: number;
  /** Cash and equivalents in millions */
  cash: number;
  /** Total assets in millions */
  total_assets: number;
  /** Total equity in millions */
  total_equity: number;
  /** Shares outstanding in millions */
  shares_outstanding: number;
  /** Sector classification */
  sector: string;
  /** Industry classification */
  industry: string;
}

/**
 * Result of a job execution.
 */
export interface JobResult {
  /** Unique job identifier */
  job_id: string;
  /** Type of job */
  job_type: JobType;
  /** Job execution status */
  status: JobStatus;
  /** Job start timestamp */
  start_time: string;
  /** Job end timestamp */
  end_time?: string | null;
  /** Timestamp of fundamental data */
  fundamentals_date?: string | null;
  /** Timestamp of market data */
  market_data_date?: string | null;
  /** Total universe size */
  universe_size?: number;
  /** Number of candidates generated */
  candidates_generated?: number;
  /** Total job duration */
  total_duration_seconds?: number;
  /** Metrics for each execution phase */
  phase_metrics?: Array<JobPhaseMetrics>;
  /** Whether job ran in degraded mode */
  degraded_mode?: boolean;
  /** Reasons for degraded mode */
  degraded_reasons?: Array<string>;
  /** Top short candidates from screening */
  top_candidates?: Array<ShortCandidate>;
  /** Error messages */
  errors?: Array<string>;
  /** Warning messages */
  warnings?: Array<string>;
}

/**
 * Market data for a ticker.
 */
export interface MarketData {
  /** Stock ticker symbol */
  ticker: string;
  /** Current stock price */
  price: number;
  /** Market capitalization in millions */
  market_cap: number;
  /** Market beta */
  beta: number;
  /** 20-day average volume */
  volume_20d_avg: number;
  /** 52-week high price */
  price_52w_high: number;
  /** 52-week low price */
  price_52w_low: number;
}

/**
 * Raw financial and market metrics for a ticker.

These metrics are computed from market and fundamental data and serve
as inputs to factor score calculations.
 */
export interface RawMetrics {
  /** Stock ticker symbol */
  ticker: string;
  /** Price-to-Sales ratio */
  price_to_sales: number;
  /** Price-to-Book ratio */
  price_to_book: number;
  /** EV/EBITDA ratio */
  ev_to_ebitda: number;
  /** Net profit margin */
  net_margin: number;
  /** EBITDA margin */
  ebitda_margin: number;
  /** Return on Equity */
  roe: number;
  /** Year-over-year revenue growth rate */
  revenue_growth: number;
  /** Debt-to-Equity ratio */
  debt_to_equity: number;
  /** Debt-to-Assets ratio */
  debt_to_assets: number;
  /** Net Debt to EBITDA ratio */
  net_debt_to_ebitda: number;
  /** Free Cash Flow margin */
  fcf_margin: number;
  /** Current ratio (liquidity) */
  current_ratio: number;
  /** Market beta */
  beta: number;
  /** Market capitalization in millions */
  market_cap: number;
  /** Distance from 52-week high as percentage */
  distance_from_52w_high: number;
  /** Sector classification */
  sector: string;
  /** Industry classification */
  industry: string;
}

/**
 * Complete screening report with all components.
 */
export interface ScreeningReport {
  /** Report metadata */
  metadata: ReportMetadata;
  /** Risk indicator scores */
  risk_indicators: RiskIndicators;
  /** Top N candidates */
  top_candidates: Array<ShortCandidate>;
  /** Candidate distribution by sector */
  sector_distribution: Array<SectorDistribution>;
  /** Candidate distribution by dominant theme */
  theme_distribution: Array<ThemeDistribution>;
  /** Statistical distributions of factor scores */
  factor_distributions: Array<FactorDistribution>;
  /** Narrative summary (optional) */
  narrative?: NarrativeSummary | null;
  /** All candidates (optional, for full data export) */
  all_candidates?: Array<ShortCandidate> | null;
}

/**
 * Configuration for a single theme.
 */
export interface ThemeConfig {
  /** Baseline weight for the theme */
  base_weight: number;
  /** Sensitivities to macro factors (downturn, inflation, liquidity) */
  sensitivities: Record<string, number>;
}
