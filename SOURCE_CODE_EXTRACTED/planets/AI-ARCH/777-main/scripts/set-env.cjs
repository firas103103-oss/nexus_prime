const fs = require('fs');
const dotenv = require('dotenv');

// Load environment variables from .env file if available
dotenv.config();

const envConfigFile = `export const environment = {
  production: true,
  supabaseUrl: '${process.env.SUPABASE_URL || ""}',
  supabaseKey: '${process.env.SUPABASE_KEY || ""}',
  geminiApiKey: '${process.env.GEMINI_API_KEY || ""}'
};
`;

const dir = './src/environments';
if (!fs.existsSync(dir)){
    fs.mkdirSync(dir, { recursive: true });
}

fs.writeFileSync(`${dir}/environment.ts`, envConfigFile);

console.log(`✅ Environment variables generated in ${dir}/environment.ts`);
console.log(`📋 Variables loaded: ${Object.keys(process.env).filter(k => k.includes('SUPABASE') || k.includes('GEMINI')).join(', ')}`);
