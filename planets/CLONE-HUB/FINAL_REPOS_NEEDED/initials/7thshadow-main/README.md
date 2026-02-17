# 📚 X-Book Smart Publisher

[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](https://github.com/firas103103-oss/x-book)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-blue.svg)]()
[![React](https://img.shields.io/badge/React-19.2-61dafb.svg)]()

## 🌟 Overview

**X-Book** is an AI-powered manuscript enhancement and publishing platform built with Gemini 3 Pro. Transform your raw manuscripts into professionally edited, publishable books with intelligent literary analysis, legal compliance audits, and automated cover generation.

### 🎯 Key Features

- **🤖 AI-Powered Editing** - Advanced manuscript enhancement using Gemini 3 Pro
- **📊 Literary Analysis** - Deep content analysis with narrative arc evaluation
- **⚖️ Legal Compliance** - Automated copyright and legal audit reports
- **🎨 Cover Generation** - Cinematic AI-generated book covers
- **📦 Complete Package** - Export TXT, HTML, and marketing materials in one ZIP
- **🌐 Multi-Language** - Full support for Arabic, English, and German
- **💾 Auto-Save** - Progressive saving with localStorage integration
- **📱 PWA Ready** - Offline support with Service Worker

---

## 📊 Project Status

**Current Version:** 4.0.0 ✅

### Deployment Status

| Platform | Status | Performance |
|----------|--------|-------------|
| **Railway** | 🟢 Production | Health Check Active |
| **Build Time** | ⚡ 5.13s | Optimized |
| **Bundle Size** | 📦 1.1 MB | Well-Split |
| **Security** | 🔒 0 Vulnerabilities | Audited |

---

## 🚀 Quick Start

### Prerequisites

- Node.js >= 20.0.0
- npm >= 10.0.0
- Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

```bash
# Clone the repository
git clone https://github.com/firas103103-oss/x-book.git
cd x-book

# Install dependencies
npm install

# Create environment file
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
# Build optimized production bundle
npm run build

# Preview production build locally
npm run preview

# Deploy (example for Railway)
./deploy.sh production
```

---

## 🏗️ Architecture

### Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **React** | UI Framework | 19.2.3 |
| **TypeScript** | Type Safety | 5.8.2 |
| **Vite** | Build Tool | 6.2.0 |
| **Tailwind CSS** | Styling | 3.4.19 |
| **Gemini AI** | AI Processing | @google/genai 1.35.0 |
| **JSZip** | File Packaging | 3.10.1 |
| **Mammoth.js** | DOCX Processing | 1.11.0 |

### Project Structure

```
x-book/
├── components/           # React components
│   ├── AIPerformanceTerminal.tsx
│   ├── ConversationEngine.tsx
│   ├── ErrorBoundary.tsx
│   ├── ProcessingEngine.tsx
│   └── ...
├── services/            # Core services
│   ├── geminiService.ts      # AI engine
│   ├── documentService.ts    # File processing
│   └── reportGeneratorService.ts
├── hooks/               # Custom React hooks
├── utils/               # Utility functions
├── types.ts             # TypeScript definitions
├── App.tsx              # Main application
└── public/              # Static assets
```

---

## 💡 Usage

### Basic Workflow

1. **Select Language** - Choose Arabic, English, or German
2. **Provide Metadata** - Enter book title, author, genre
3. **Upload Manuscript** - Upload DOCX or TXT file
4. **Choose Goals** - Select editing style and intensity
5. **AI Processing** - Automated analysis, editing, and enhancement
6. **Download Package** - Get complete publishing package (ZIP)

### Output Package Includes

- 📄 **Edited Manuscript** (TXT + HTML)
- 📊 **Literary Analysis Report**
- ⚖️ **Legal Compliance Audit**
- 📝 **Editor's Strategic Notes**
- 🎨 **High-Resolution Cover Art**
- 📢 **Marketing Materials** (Synopsis, Blurb)
- 📜 **Official Certificate** from The Seventh Shadow

---

## 📈 Performance

- **Build Time:** 5.13 seconds
- **Bundle Size:** 1.1 MB (optimized, code-split)
- **Lighthouse Score:** [Run for metrics]
- **Security:** 0 vulnerabilities
- **Type Coverage:** 100% TypeScript

### Bundle Analysis

| Chunk | Size | Gzipped | Type |
|-------|------|---------|------|
| index.js | 58 KB | 21 KB | Main |
| vendor-react | 201 KB | 63 KB | React ecosystem |
| vendor-ai | 254 KB | 50 KB | Gemini AI |
| vendor-docs | 154 KB | 48 KB | Document processing |
| vendor-common | 347 KB | 83 KB | Utilities |

---

## 🔒 Security

- ✅ **0 Vulnerabilities** (npm audit)
- ✅ **API Key Protection** (environment variables)
- ✅ **Input Validation** (all user inputs)
- ✅ **Secure File Processing** (no code execution)
- ✅ **HTTPS Enforcement** (production)

See [SECURITY.md](SECURITY.md) for detailed security policy.

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Type check
npm run lint

# Build
npm run build

# Clean
npm run clean
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Gemini AI** - Powering the intelligence
- **MrF X OS Organization** - Project sponsor
- **The Seventh Shadow** - AI Agent persona

---

## 📞 Support

For support, questions, or feature requests:
- 📧 Email: support@mrfxos.org
- 🐛 Issues: [GitHub Issues](https://github.com/firas103103-oss/x-book/issues)
- 📖 Documentation: [Full Stack Analysis](FULL_STACK_ANALYSIS.md)

---

## 🗺️ Roadmap

### ✅ Completed
- Multi-language support (AR, EN, DE)
- AI-powered editing and analysis
- Cover generation
- PWA support
- Production deployment

### 🔄 In Progress
- E2E testing
- Performance monitoring
- Analytics integration

### 📋 Planned
- Dark mode
- More language support
- Mobile app
- API documentation

---

**Made with ❤️ by MrF X OS Organization**

**Powered by Gemini 3 Pro** 🤖
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**firas103103-oss**

- GitHub: [@firas103103-oss](https://github.com/firas103103-oss)

---

*Last Updated: 2026-01-14*
