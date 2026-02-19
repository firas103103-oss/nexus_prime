import { Router } from 'express';
import FinancialController from '../controllers/financialController';

const setFinancialRoutes = (router: Router) => {
    const financialController = new FinancialController();

    router.get('/financial', financialController.getFinancialData);
    router.post('/financial', financialController.updateFinancialData);
};

export default setFinancialRoutes;