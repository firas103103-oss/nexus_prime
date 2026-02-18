# 🤝 Contributing to NEXUS PRIME

Thank you for your interest in contributing to NEXUS PRIME! This document provides guidelines for contributing to the project.

---

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

---

## Getting Started

### 1. Fork the Repository

```bash
# Fork via GitHub UI, then clone your fork
git clone git@github.com:YOUR_USERNAME/nexus_prime.git
cd nexus_prime
```

### 2. Set Up Development Environment

```bash
# Install dependencies
pip install -r requirements.txt  # For Python projects
npm install                      # For Node.js projects

# Start local services
cd /root/nexus_prime
docker compose up -d
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

---

## Project Structure

```
NEXUS_PRIME_UNIFIED/
├── dashboard-arc/      # React admin dashboard
├── planets/            # AI agent configurations
├── integration/        # Integration modules
├── products/           # Standalone products
├── scripts/            # Automation scripts
├── docs/               # Documentation
└── n8n-workflows/      # Workflow definitions
```

---

## Commit Guidelines

### Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code style (formatting, etc.) |
| `refactor` | Code refactoring |
| `test` | Adding tests |
| `chore` | Maintenance tasks |

### Examples

```bash
feat(planets): add new AI agent for customer support
fix(nexus-voice): resolve shell injection vulnerability
docs(readme): update installation instructions
```

---

## Pull Request Process

### 1. Update Your Branch

```bash
git fetch origin
git rebase origin/main
```

### 2. Run Tests

```bash
bash scripts/final_test.sh
# Ensure: 41/41 tests pass
```

### 3. Push Changes

```bash
git push origin feature/your-feature-name
```

### 4. Create Pull Request

- Go to GitHub and create a PR
- Fill in the PR template
- Request review from maintainers

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass (41/41)
- [ ] Documentation updated if needed
- [ ] No sensitive data (API keys, passwords)
- [ ] Commit messages follow guidelines

---

## Development Guidelines

### Python Code

```python
# Use type hints
def process_data(input: str) -> dict:
    """Process input data and return results."""
    pass

# Use environment variables for secrets
import os
api_key = os.getenv('API_KEY', '')

# Never hardcode credentials
# BAD: api_key = "sk-proj-xxxxx"
# GOOD: api_key = os.getenv('OPENAI_API_KEY')
```

### JavaScript/TypeScript

```typescript
// Use async/await
async function fetchData(): Promise<Data> {
  const response = await fetch(url);
  return response.json();
}

// Use environment variables
const apiKey = process.env.API_KEY || '';
```

### Docker

```yaml
# Use specific image tags
image: postgres:15.1.0.147

# Set resource limits
deploy:
  resources:
    limits:
      memory: 512M
```

---

## Security Guidelines

### DO:
- Use environment variables for secrets
- Validate user inputs
- Use parameterized queries
- Follow least privilege principle

### DON'T:
- Commit API keys or passwords
- Use `shell=True` in subprocess calls
- Trust user input without validation
- Expose internal services to the internet

---

## Testing

### Running Tests

```bash
# Full test suite
bash scripts/final_test.sh

# Quick status check
bash scripts/STATUS.sh
```

### Test Categories

1. **Infrastructure Tests** - Docker services, ports
2. **Health Tests** - Container health status
3. **Connectivity Tests** - Service communication
4. **Integration Tests** - API endpoints
5. **Security Tests** - UFW, SSL

---

## Documentation

### When to Update Docs

- Adding new features
- Changing existing behavior
- Fixing documentation bugs
- Adding examples

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `MASTER_DOCUMENTATION.md` | Complete reference |
| `docs/ARCHITECTURE.md` | Technical architecture |
| `docs/QUICKSTART.md` | Getting started |
| `DEPLOYMENT.md` | Deployment guide |

---

## Reporting Issues

### Bug Reports

Include:
- Clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative solutions considered

---

## Questions?

- **Email**: admin@mrf103.com
- **GitHub Issues**: For bugs and features
- **Documentation**: Check docs first

---

## License

By contributing, you agree that your contributions will be licensed under the project's license.

---

*Thank you for contributing to NEXUS PRIME! 🌌*
