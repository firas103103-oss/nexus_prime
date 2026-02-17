import { Request, Response, NextFunction } from 'express';

export class APIError extends Error {
  statusCode: number;
  
  constructor(message: string, statusCode: number = 500) {
    super(message);
    this.statusCode = statusCode;
    this.name = 'APIError';
  }
}

export function errorHandler(
  err: Error | APIError,
  req: Request,
  res: Response,
  next: NextFunction
) {
  console.error('❌ Error:', err);

  if (err instanceof APIError) {
    return res.status(err.statusCode).json({
      error: err.message,
      status: err.statusCode
    });
  }

  // Default error
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined,
    status: 500
  });
}
