import { Request, Response } from 'express';
import FinancialService from '../services/financialService';

class FinancialController {
    private financialService: FinancialService;

    constructor() {
        this.financialService = new FinancialService();
    }

    public async getFinancialData(req: Request, res: Response): Promise<void> {
        try {
            const data = await this.financialService.retrieveFinancialData();
            res.status(200).json(data);
        } catch (error) {
            res.status(500).json({ message: 'Error retrieving financial data', error });
        }
    }

    public async updateFinancialData(req: Request, res: Response): Promise<void> {
        try {
            const updatedData = await this.financialService.updateFinancialData(req.body);
            res.status(200).json(updatedData);
        } catch (error) {
            res.status(500).json({ message: 'Error updating financial data', error });
        }
    }
}

export default FinancialController;