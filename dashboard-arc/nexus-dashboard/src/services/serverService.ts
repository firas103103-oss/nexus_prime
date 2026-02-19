export class ServerService {
    private serverStatus: string;
    private eventLog: string[];

    constructor() {
        this.serverStatus = 'Unknown';
        this.eventLog = [];
    }

    public checkServerHealth(): string {
        // Logic to check server health
        // This is a placeholder for actual health check logic
        this.serverStatus = 'Healthy'; // Example status
        this.logEvent('Checked server health');
        return this.serverStatus;
    }

    public updateServerStatus(newStatus: string): void {
        this.serverStatus = newStatus;
        this.logEvent(`Server status updated to: ${newStatus}`);
    }

    private logEvent(event: string): void {
        const timestamp = new Date().toISOString();
        this.eventLog.push(`[${timestamp}] ${event}`);
    }

    public getEventLog(): string[] {
        return this.eventLog;
    }
}