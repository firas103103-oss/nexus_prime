// This file contains the JavaScript code for client-side interactions, handling events and updating the dashboard dynamically.

document.addEventListener('DOMContentLoaded', () => {
    // Initialize components
    const serverStatus = new ServerStatus();
    const financialConditions = new FinancialConditions();
    const marketingAnalytics = new MarketingAnalytics();

    // Fetch and display server status
    function updateServerStatus() {
        serverStatus.fetchStatus().then(status => {
            document.getElementById('server-status').innerText = status;
        });
    }

    // Fetch and display financial conditions
    function updateFinancialConditions() {
        financialConditions.fetchData().then(data => {
            document.getElementById('financial-conditions').innerText = JSON.stringify(data);
        });
    }

    // Fetch and display marketing analytics
    function updateMarketingAnalytics() {
        marketingAnalytics.fetchData().then(data => {
            document.getElementById('marketing-analytics').innerText = JSON.stringify(data);
        });
    }

    // Set up periodic updates
    setInterval(updateServerStatus, 5000); // Update server status every 5 seconds
    setInterval(updateFinancialConditions, 60000); // Update financial conditions every minute
    setInterval(updateMarketingAnalytics, 60000); // Update marketing analytics every minute

    // Initial fetch
    updateServerStatus();
    updateFinancialConditions();
    updateMarketingAnalytics();
});