export interface Endpoint {
  id: number;
  name: string;
  url: string;
  method: string;
  headers: string | null;
  body: string | null;
  expected_status: number;
  created_at: string;
}

export interface EndpointStatus {
  endpoint: Endpoint;
  current_status: boolean;
  last_check: string | null;
  response_time: number | null;
  uptime_90d: number;
}

export interface DailyUptime {
  date: string;
  uptime_percentage: number;
  total_checks: number;
  successful_checks: number;
}

export interface EndpointHistory {
  endpoint: Endpoint;
  daily_uptimes: DailyUptime[];
}

export interface OverallStatus {
  status: 'operational' | 'partial_outage' | 'major_outage';
  message: string;
  endpoints: EndpointStatus[];
}
