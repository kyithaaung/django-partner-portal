# Security and Access-Control Suggestions

This portal enforces tenant isolation by routing partner business data to a separate MySQL instance (`partner`) while keeping internal identity/admin records in `default`.

## Role model

- **Partner users** (`PartnerUserProfile`) can only access data belonging to their own `Partner`.
- **Internal users** (`InternalUserProfile`, MS/dev roles) can view and operate across all partners.

## Recommended hardening for production

1. Set `DJANGO_DEBUG=false`.
2. Use strong, rotated `DJANGO_SECRET_KEY`.
3. Force HTTPS and set `SECURE_SSL_REDIRECT=True` behind a trusted proxy.
4. Enable HSTS (`SECURE_HSTS_SECONDS`, preload, include_subdomains).
5. Store credentials in a secrets manager (Vault, AWS Secrets Manager, etc.).
6. Add MFA/SSO for internal users.
7. Restrict MySQL network access so only application containers can connect.
8. Add audit logging for login attempts, STO creation, and stock changes.
9. Add rate-limiting on `/login/` and lockout thresholds.
10. Run periodic tenant-isolation tests to ensure no cross-partner leakage.

## Partner container split

`docker-compose.yml` includes:

- `mysql_internal`: internal/auth/admin data.
- `mysql_partner`: partner tenant data.

For stronger isolation, run one partner DB per partner (or schema-per-partner) and add a tenant-aware database router.
