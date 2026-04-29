# OWASP Top 10 Patterns to Detect

## A01 — Broken Access Control
- Functions that skip authorization checks
- Direct object references without ownership validation
- Missing role checks before sensitive operations

## A02 — Cryptographic Failures
- Hardcoded passwords, API keys, tokens, secrets
- Use of MD5/SHA1 for password hashing
- HTTP instead of HTTPS for sensitive endpoints
- Weak random number generation (Math.random, random.random for crypto)

## A03 — Injection
- SQL queries built with string concatenation using user input
- Shell commands with unsanitized user input (os.system, subprocess with shell=True)
- LDAP/XPath/NoSQL injection patterns

## A05 — Security Misconfiguration
- Debug mode enabled in production code
- Default credentials in config files
- Overly permissive CORS (Access-Control-Allow-Origin: *)
- Stack traces exposed to users

## A07 — Identification & Auth Failures
- Weak session management
- Missing rate limiting on login endpoints
- Passwords stored in plain text or reversible encryption
- JWT without expiry or with 'none' algorithm

## A09 — Logging Failures
- Sensitive data (passwords, tokens) logged to console/file
- Missing audit logs for security-sensitive actions

## A10 — SSRF
- User-controlled URLs passed directly to HTTP clients
- Missing allowlists for outbound requests
