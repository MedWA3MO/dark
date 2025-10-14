# Insecure Client-Side Admin Check (Cookie Tampering)

**Target Page:** `http://localhost:8080/index.php?page=signin`  

```bash
curl 'http://localhost:8080/index.php?page=signin&username=&password=&Login=Login' \
  -b 'I_am_admin=b326b5062b2f0e69046810717534cb09'
```

---

## 1. What the Vulnerability Is (Classification, OWASP)

* **Vulnerability Name:** Client-side Trust / Cookie Tampering that Controls Authorization
* **OWASP Classification:** **Broken Access Control** (OWASP Top 10 — A01: Broken Access Control)

The application relies on a client-supplied cookie value to decide whether the user is an admin. An attacker can modify that cookie and gain privileged access.

---

## 2. Root Cause / Security Flaw

* The server **trusts an unauthenticated client-side value** (`I_am_admin`) to determine admin privileges.
* The server accepts a raw or predictable hashed value (e.g., `md5("true")` or a static hash)  as proof of admin status.
* In short: **Authorization decisions are made solely based on user-controlled data** rather than on server-validated sessions/permissions.

---

## 3. How I Exploited It (Step-by-Step, Minimal)

1. Observed the signin request and cookies. The application sets/reads a cookie named `I_am_admin`. Example observed cookie value:
   ```
   I_am_admin=b326b5062b2f0e69046810717534cb09
   ```
   (This value is the MD5 of the literal string `false`.)
  
2. Hypothesis: The server checks `I_am_admin` to allow admin-only actions. If we can present a “true” value (or the expected hashed value), the server might treat us as admin.

3. Crafted a request with the cookie set to the expected hashed value and sent it to the signin page:

   ```bash
   curl 'http://localhost:8080/index.php?page=signin&username=&password=&Login=Login' \
     -b 'I_am_admin=b326b5062b2f0e69046810717534cb09'
   ```

4. The server responded as if the requester was admin and revealed the flag.

---

## 4. What the Impact Could Be

* **Full Admin Privilege Escalation:** The attacker can perform admin-only actions (view secrets, read flags, change data).
* **Data Exfiltration:** Access to sensitive data (user lists, configuration, secrets).
* **Persistence & Pivoting:** Modifying server state, creating backdoors, or adding privileged users.
* **Trust & Integrity Failure:** Breaks the security model — the client should not be able to escalate privileges by changing cookies.
* **Overall Severity:** **High / Critical**, depending on what admin actions enable on that application.

---

## 5. How to Fix It (Patch / Concrete Recommendations)

### Core Principle

**Never make authorization decisions solely based on client-side values.** The server must validate identity and permissions using server-controlled state or cryptographically protected tokens.

### Immediate Fixes (Short-Term)

* **Stop trusting `I_am_admin` cookie:** Remove logic that reads this cookie and grants privileges directly.
* **Require proper server-side session authentication** for admin actions (e.g., `$_SESSION['is_admin']` set on the server after a secure login).
* If you must store authorization state on the client, **use a signed cookie** (HMAC) or JWT with server-side verification and a secret key — and still validate user session server-side.
