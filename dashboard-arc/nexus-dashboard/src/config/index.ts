// Configuration settings for the application
export const config = {
    environment: process.env.NODE_ENV || 'development',
    port: process.env.PORT || 3000,
    database: {
        host: process.env.DB_HOST || 'localhost',
        port: process.env.DB_PORT || 5432,
        user: process.env.DB_USER || 'user',
        password: process.env.DB_PASSWORD || 'password',
        database: process.env.DB_NAME || 'nexus_db',
    },
    api: {
        baseUrl: process.env.API_BASE_URL || 'http://localhost:3000/api',
    },
    logging: {
        level: process.env.LOG_LEVEL || 'info',
    },
};