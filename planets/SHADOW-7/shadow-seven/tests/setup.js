import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';
import 'fake-indexeddb/auto';

// Set environment variables for Vite
globalThis.__VITE_TEST_ENV__ = true;

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock postgresClient (local API)
vi.mock('@/api/postgresClient', () => ({
  supabase: null,
  db: {
    manuscripts: {
      list: vi.fn().mockResolvedValue([]),
      get: vi.fn().mockResolvedValue(null),
      create: vi.fn().mockResolvedValue({}),
      update: vi.fn().mockResolvedValue({}),
      delete: vi.fn().mockResolvedValue({ success: true }),
      filter: vi.fn().mockResolvedValue([]),
    },
    complianceRules: { list: vi.fn().mockResolvedValue([]), create: vi.fn(), update: vi.fn(), delete: vi.fn() },
    coverDesigns: { create: vi.fn().mockResolvedValue({}) },
    processingJobs: { filter: vi.fn().mockResolvedValue([]) },
  },
  auth: {
    getUser: vi.fn().mockResolvedValue(null),
    signIn: vi.fn(),
    signUp: vi.fn(),
    signOut: vi.fn(),
    updateUser: vi.fn(),
  },
  storage: {
    uploadFile: vi.fn().mockResolvedValue({ file_url: 'test', path: 'test' }),
    deleteFile: vi.fn(),
    getPublicUrl: vi.fn((_, p) => p),
  },
}));

// Mock Gemini client
vi.mock('@/api/geminiClient', () => ({
  gemini: {
    invokeLLM: vi.fn().mockResolvedValue({ output: 'test' }),
    generateContent: vi.fn().mockResolvedValue('test'),
  },
  default: {
    invokeLLM: vi.fn().mockResolvedValue({ output: 'test' }),
  },
}));

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return [];
  }
  unobserve() {}
};

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};

// Mock IndexedDB if not already available
if (!global.indexedDB) {
  const fakeIndexedDB = require('fake-indexeddb');
  global.indexedDB = fakeIndexedDB;
  global.IDBDatabase = fakeIndexedDB.IDBDatabase;
  global.IDBFactory = fakeIndexedDB.IDBFactory;
  global.IDBKeyRange = fakeIndexedDB.IDBKeyRange;
  global.IDBObjectStore = fakeIndexedDB.IDBObjectStore;
  global.IDBRequest = fakeIndexedDB.IDBRequest;
  global.IDBTransaction = fakeIndexedDB.IDBTransaction;
}
