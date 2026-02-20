export class MarketingController {
    constructor(private marketingService: MarketingService) {}

    async getMarketingData(req, res) {
        try {
            const data = await this.marketingService.fetchMarketingData();
            res.status(200).json(data);
        } catch (error) {
            res.status(500).json({ message: 'Error fetching marketing data', error });
        }
    }

    async updateMarketingData(req, res) {
        try {
            const updatedData = await this.marketingService.updateMarketingData(req.body);
            res.status(200).json(updatedData);
        } catch (error) {
            res.status(500).json({ message: 'Error updating marketing data', error });
        }
    }
}