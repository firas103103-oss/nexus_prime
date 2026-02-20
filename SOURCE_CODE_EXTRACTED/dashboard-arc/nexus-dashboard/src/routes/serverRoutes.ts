import { Router } from 'express';
import { ServerController } from '../controllers/serverController';

const router = Router();
const serverController = new ServerController();

export function setServerRoutes(app: Router) {
    app.use('/api/server', router);
    
    router.get('/status', serverController.getServerStatus.bind(serverController));
    router.post('/status', serverController.updateServerStatus.bind(serverController));
}