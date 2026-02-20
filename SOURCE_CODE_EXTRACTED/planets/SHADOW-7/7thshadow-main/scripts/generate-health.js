import fs from 'fs';
import { execSync } from 'child_process';
import path from 'path';
import { readFileSync } from 'fs';

const pkg = JSON.parse(readFileSync('./package.json', 'utf8'));

let commit = null;
try {
  commit = execSync('git rev-parse --short HEAD').toString().trim();
} catch (e) {
  commit = null;
}

const out = {
  status: 'ok',
  timestamp: new Date().toISOString(),
  service: pkg.name || 'x-book-smart-publisher',
  version: pkg.version || null,
  commit: commit
};

import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const outDir = path.resolve(__dirname, '..', 'dist');
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

fs.writeFileSync(path.join(outDir, 'health.json'), JSON.stringify(out, null, 2));
console.log('Generated dist/health.json', out);
