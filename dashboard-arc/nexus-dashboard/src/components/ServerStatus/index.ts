class ServerStatus {
    constructor() {
        this.healthMetrics = {
            uptime: 0,
            responseTime: 0,
            status: 'unknown',
        };
    }

    fetchServerStatus() {
        // Simulate fetching server status from an API or service
        return new Promise((resolve) => {
            setTimeout(() => {
                this.healthMetrics = {
                    uptime: Math.random() * 100,
                    responseTime: Math.random() * 200,
                    status: 'operational',
                };
                resolve(this.healthMetrics);
            }, 1000);
        });
    }

    updateServerStatus(newMetrics) {
        this.healthMetrics = { ...this.healthMetrics, ...newMetrics };
    }

    getServerStatus() {
        return this.healthMetrics;
    }
}

export default ServerStatus;