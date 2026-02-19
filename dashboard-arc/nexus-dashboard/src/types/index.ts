// This file exports interfaces and types used throughout the application, such as ServerStatus, FinancialData, and MarketingMetrics.

export interface ServerStatus {
    uptime: number; // in seconds
    health: string; // e.g., 'healthy', 'degraded', 'down'
    lastChecked: Date; // timestamp of the last health check
}

export interface FinancialData {
    revenue: number; // total revenue
    expenses: number; // total expenses
    profit: number; // total profit
    lastUpdated: Date; // timestamp of the last financial update
}

export interface MarketingMetrics {
    campaignName: string; // name of the marketing campaign
    impressions: number; // total impressions
    clicks: number; // total clicks
    conversionRate: number; // percentage of conversions
    lastAnalyzed: Date; // timestamp of the last analysis
}