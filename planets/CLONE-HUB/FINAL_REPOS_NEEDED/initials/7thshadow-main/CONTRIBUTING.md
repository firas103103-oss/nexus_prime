# Contributing to X-Book

Thank you for considering contributing to X-Book! This document outlines the process for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and professional environment.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots if applicable
- Your environment (browser, OS, Node version)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- A clear description of the enhancement
- Why this enhancement would be useful
- Any potential implementation ideas

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test your changes**: `npm run build && npm run preview`
5. **Commit with clear messages**: `git commit -m "Add amazing feature"`
6. **Push to your fork**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## Development Setup

```bash
# Clone the repository
git clone https://github.com/firas103103-oss/x-book.git
cd x-book

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Add your GEMINI_API_KEY

# Start development server
npm run dev
```

## Code Style

- Use TypeScript for type safety
- Follow React best practices
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

## Testing

Before submitting a PR:
- Test the build: `npm run build`
- Test the production preview: `npm run preview`
- Ensure no console errors in production build
- Test on multiple browsers if UI changes

## Project Structure

```
x-book/
├── components/       # React components
├── services/         # API services (Gemini, document processing)
├── hooks/           # Custom React hooks
├── utils/           # Utility functions
├── types.ts         # TypeScript types
├── App.tsx          # Main application
└── public/          # Static assets
```

## Commit Message Format

Use clear, descriptive commit messages:
- `feat: Add new feature`
- `fix: Fix bug in component`
- `docs: Update documentation`
- `style: Format code`
- `refactor: Refactor service`
- `test: Add tests`
- `chore: Update dependencies`

## Questions?

Feel free to open an issue for any questions about contributing.

Thank you for your contributions! 🎉
