import express from 'express';
import { setServerRoutes } from './routes/serverRoutes';
import { setFinancialRoutes } from './routes/financialRoutes';
import { setMarketingRoutes } from './routes/marketingRoutes';
import { json } from 'body-parser';
import { config } from './config';

const app = express();
const PORT = config.port || 3000;

// Middleware
app.use(json());
app.use(express.static('public'));

// Routes
setServerRoutes(app);
setFinancialRoutes(app);
setMarketingRoutes(app);

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});