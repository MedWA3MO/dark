
# 🛡️ Restrict Access Vulnerability

## 1. How did I spot the vulnerability?

Fetched `htpasswd` and inspected it:

```bash
curl -s http://localhost:8080/htpasswd
# Output:
# User-agent: *
# Disallow: /whatever
# Disallow: /.hidden


The `Disallow` entries revealed hidden directories.

Navigated to `/whatever/` and discovered a publicly accessible `.htpasswd`:

```bash
curl -s http://localhost:8080/whatever/htpasswd
# Output:
# root:437394baff5aa33daa618be47b75cb49
```

Identified the hash as MD5 (via hash identifier / online lookup) and recovered the password `qwerty123@`.

Used the credentials to access the admin area (common URL `/admin`) and retrieved the flag:

```bash
curl -s -u root:qwerty123@ http://localhost:8080/admin | grep -i flag
# flag: <REDACTED-FLAG-FROM-ADMIN>
```

---

## 2. What is the vulnerability?

**Restrict Access / Information Disclosure (Misconfiguration)** - The application exposes sensitive locations through `htpasswd` and leaves credential material (`.htpasswd`) accessible in the web root. Attackers can discover, crack, and reuse credentials to access admin pages.

---

## 3. Why does it exist (the security flaw)?

- `htpasswd` was used to hide sensitive directories instead of protecting them — attackers read it as a **roadmap**
- **Sensitive files** (`.htpasswd`) were stored under a publicly accessible path
- **Weak hashing algorithm** (MD5) was used for passwords, enabling quick cracking via lookup/decryption services
- **Access controls relied on obscurity** and file location rather than robust server-side authentication/authorization

---

## 4. What could the impact be?

- **Full or partial unauthorized administrative access**
- **Disclosure or modification of sensitive data** (configuration, secrets, user data)
- **Lateral movement and privilege escalation** within the system
- **Reputational damage** and potential compliance violations

---

## 5. How to fix it (patch)?

**Never rely on `htpasswd` or obscurity for security.** Instead:

- **Remove sensitive entries from `htpasswd`** - treat it as SEO-only, not a security control
- **Move `.htpasswd` and configuration files outside the web root** (in a non-served directory)
- **Prevent direct access to sensitive files** via web server configuration:

**Apache Example:**
```
<FilesMatch "^\.ht">
  Require all denied
</FilesMatch>
```

**Nginx Example:**
```
location ~ /\. {
  deny all;
  access_log off;
  log_not_found off;
}
```

- **Use strong, salted password hashing** (e.g., bcrypt, Argon2) - never use MD5 for passwords
- **Implement proper session-based authentication** with server-side validation
- **Apply least privilege** and remove unnecessary public exposures
- **Audit regularly** - run automated scanners to detect exposed sensitive files

---

## 6. Vulnerability classification (OWASP)

**A01 - Broken Access Control / Information Disclosure** - Exposure of sensitive files and reliance on client-side or obscurity-based security, combined with weak credential storage and poor access management.