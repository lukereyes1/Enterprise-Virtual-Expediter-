/**
 * Type definitions for ShortScreen Command mobile app
 */

// API Response Types

export interface RegimeStatus {
  status: 'risk_off' | 'neutral' | 'risk_on';
  risk_off_score: number;
  small_cap_stress_score: number;
  avg_beta: number;
}

export interface ThemeSummary {
  name: string;
  display_name: string;
  score: number;
  trend: 'up' | 'down' | 'flat';
  top_decile_count: number;
  score_change_24h: number;
}

export interface DataFreshness {
  fundamentals_updated_at: string;
  market_data_updated_at: string;
}

export interface StatusResponse {
  timestamp: string;
  regime: RegimeStatus;
  themes: ThemeSummary[];
  data_freshness: DataFreshness;
}

export interface EventData {
  [key: string]: any;
}

export interface Event {
  id: string;
  type: 'regime_change' | 'theme_spike' | 'ticker_alert' | 'system_alert';
  title: string;
  body: string;
  created_at: string;
  read: boolean;
  priority: 'low' | 'medium' | 'high';
  data: EventData;
}

export interface EventsResponse {
  events: Event[];
  pagination: {
    total: number;
    page: number;
    per_page: number;
  };
}

export interface ThemeDetail {
  name: string;
  display_name: string;
  description: string;
  score: number;
  top_decile_count: number;
  sector_distribution: Record<string, number>;
  factor_vs_universe: {
    valuation: number;
    profitability: number;
    growth: number;
  };
}

export interface TickerName {
  ticker: string;
  company_name: string;
  sector: string;
  market_cap: number;
  global_score: number;
  theme_score: number;
  in_top_decile: boolean;
}

export interface ThemeNamesResponse {
  names: TickerName[];
}

export interface HistoryPoint {
  date: string;
  score: number;
  top_decile_count?: number;
  in_top_decile?: boolean;
}

export interface ThemeHistoryResponse {
  history: HistoryPoint[];
}

export interface FactorScores {
  leverage: number;
  valuation: number;
  beta: number;
  quality: number;
  growth: number;
  duration: number;
}

export interface TickerDetail {
  ticker: string;
  company_name: string;
  sector: string;
  market_cap: number;
  global_score: number;
  in_top_decile: boolean;
  factor_scores: FactorScores;
  theme_scores: Record<string, number>;
  primary_theme: string;
  days_in_top_decile: number;
}

export interface TickerHistoryResponse {
  history: HistoryPoint[];
}

export interface AlertSettings {
  score_threshold: number;
  notify_on_entry: boolean;
  notify_on_exit: boolean;
  notify_on_factor_spike: boolean;
}

export interface Watchlist {
  id: string;
  user_id: string;
  name: string;
  description: string;
  created_at: string;
  alert_settings: AlertSettings;
  tickers?: TickerName[];
  stats?: {
    avg_score: number;
    theme_distribution: Record<string, number>;
  };
}

export interface WatchlistsResponse {
  watchlists: Watchlist[];
}

export interface UserPreferences {
  alert_types: {
    regime_changes: boolean;
    theme_spikes: boolean;
    new_top_decile: boolean;
    watchlist_alerts: boolean;
    system_issues: boolean;
  };
  max_alerts_per_day: number;
  digest_mode: boolean;
  market_hours_only: boolean;
  timezone: string;
}

export interface User {
  id: string;
  email: string;
  created_at: string;
}

// Navigation Types

export type RootStackParamList = {
  Main: undefined;
  TickerDetail: { ticker: string };
  ThemeDetail: { themeName: string };
  WatchlistDetail: { watchlistId: string };
  EventDetail: { eventId: string };
};

export type MainTabParamList = {
  Home: undefined;
  Alerts: undefined;
  Themes: undefined;
  Watchlists: undefined;
  Settings: undefined;
};

// Component Prop Types

export interface FactorBarChartProps {
  scores: FactorScores;
  height?: number;
}

export interface ThemeTileProps {
  theme: ThemeSummary;
  onPress: () => void;
}

export interface EventCardProps {
  event: Event;
  onPress: () => void;
}

export interface TickerRowProps {
  ticker: TickerName;
  onPress: () => void;
  showSwipeAction?: boolean;
  onSwipeAction?: () => void;
}
