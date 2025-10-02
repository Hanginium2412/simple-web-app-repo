1. Container hardening

	- Use minimal base image (python:3.12-slim).

	- Use a non-root user in container (useradd appuser).

	- Multi-stage build if building assets; reduce final image size.

	- Drop Linux capabilities and set read-only filesystem in production.

	- Scan images in CI with Trivy (add aquasecurity/trivy-action step).

2. Secrets & credentials

	- Do NOT commit .env with real secrets. Use Docker secrets (Swarm/Kubernetes secrets) or Vault.

	- Put DB password and Docker registry tokens in GitHub Secrets.

3. Network & access control

	- Run DB on private network only; only web has access to DB.

	- Use firewall/iptables / UFW to restrict ports.

	- TLS termination at edge (reverse proxy like Traefik or Nginx with Let’s Encrypt).

4. Least privilege

	- DB user with only INSERT/SELECT privileges on submissions table (create separate migration to set privileges).

	- Limit SSH users; use key-based auth.

5. Audit & compliance

	- Enable access/audit logs for DB and containers.

	- Data protection: encryption at rest (cloud provider or disk encryption) and TLS in transit (TLS for Postgres).

	- GDPR: minimize stored personal data, retention policy, rights-to-forget workflow.
