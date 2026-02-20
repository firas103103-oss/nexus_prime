# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow these steps:

### 1. **Do NOT** create a public GitHub issue

Security vulnerabilities should be reported privately to prevent exploitation.

### 2. Report via GitHub Security Advisories

1. Go to the [Security tab](../../security/advisories)
2. Click "Report a vulnerability"
3. Fill in the details:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### 3. Or email directly

Send details to: **security@nexus-prime.com** (replace with actual email)

**Please include:**
- Description of the vulnerability
- Affected versions
- Steps to reproduce
- Proof of concept (if applicable)
- Your contact information

### 4. Response Timeline

- **Initial Response:** Within 48 hours
- **Status Update:** Within 7 days
- **Fix Timeline:** Depends on severity
  - Critical: 1-3 days
  - High: 7-14 days
  - Medium: 30 days
  - Low: 90 days

## Security Best Practices

### For Deployment

1. **Use strong passwords** for all services
   ```bash
   openssl rand -base64 32
   ```

2. **Enable TLS/SSL** for all external connections
   ```yaml
   # docker-compose.yml
   environment:
     - FORCE_SSL=true
   ```

3. **Limit network exposure**
   - Only expose necessary ports
   - Use firewall rules
   - Deploy in private VPC

4. **Regular updates**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

5. **Backup encryption**
   ```bash
   gpg --encrypt nexus_backup.sql
   ```

### For Development

1. **Never commit secrets**
   - Use `.env` files (in `.gitignore`)
   - Use environment variables
   - Use secret management tools

2. **Review dependencies**
   ```bash
   pip audit
   npm audit
   ```

3. **Use pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Known Security Features

### RS256 JWT

- Asymmetric signing with 2048-bit RSA
- Public key via JWKS endpoint
- 24-hour token expiry
- Key rotation support

### Data Sovereignty

- 100% local AI processing (no external APIs)
- LiteLLM proxy blocks external calls
- All data stays on your infrastructure

### Database Security

- Password authentication required
- Connection pooling with limits
- Prepared statements (SQL injection protection)
- Regular backups

### Redis Security

- `requirepass` authentication
- AOF persistence
- Memory limits
- Network isolation

## Security Audit History

| Date | Auditor | Findings | Status |
|------|---------|----------|--------|
| 2026-02 | Internal | Initial review | ✅ Addressed |

## Vulnerability Disclosure

When a vulnerability is fixed:

1. **Private disclosure** to reporter
2. **Patch release** with security tag
3. **Public disclosure** after 7-day grace period
4. **CVE assignment** (if applicable)

## Contact

- Security issues: security@nexus-prime.com
- General inquiries: contact@nexus-prime.com
- GitHub: [@mrf103](https://github.com/mrf103)

---

**Thank you for helping keep NEXUS PRIME secure!** 🔒
