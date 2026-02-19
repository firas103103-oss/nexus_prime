import { Router } from 'express';
import { MarketingController } from '../controllers/marketingController';

const marketingRouter = Router();
const marketingController = new MarketingController();

export function setMarketingRoutes(app: Router) {
    app.use('/api/marketing', marketingRouter);

    marketingRouter.get('/data', marketingController.getMarketingData.bind(marketingController));
    marketingRouter.post('/data', marketingController.updateMarketingData.bind(marketingController));
}