# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please send an email to security@mrfxos.org. All security vulnerabilities will be promptly addressed.

Please do not publicly disclose the issue until it has been addressed by the team.

## Security Best Practices

When using this application:

1. **API Keys**: Never commit your `GEMINI_API_KEY` to version control
2. **Environment Variables**: Always use `.env` files (not committed to git) for sensitive data
3. **Updates**: Keep dependencies updated regularly with `npm audit fix`
4. **HTTPS**: Always deploy the application over HTTPS in production
5. **Content Security**: Be cautious when processing user-uploaded documents

## Known Security Measures

- Input validation on all user inputs
- Secure file processing with mammoth.js
- No direct execution of user code
- Rate limiting recommendations for API calls
- Content Security Policy headers in production
