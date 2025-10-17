# Path Traversal / Directory Traversal (file disclosure)

## 1) What the vulnerability is (OWASP classification)

**Vulnerability name:** Path Traversal (a.k.a. Directory Traversal) — arbitrary file read via crafted path input.

**OWASP Top 10 (2021) classification:**
**A01 — Broken Access Control.**

* Why: The application allows users to access files outside intended directories because access control and path validation are missing or insufficient. Attackers can bypass intended restrictions and read arbitrary files on the system.

(You may also note **A05 Security Misconfiguration** as related: exposing files or allowing direct filesystem access without restrictions stems from misconfiguration/unsafe defaults.)

---

## 2) root cause / security flaw

* **Untrusted input used directly:** The application takes a user-controlled path (URL parameter or form field) and uses it to open files without properly validating or canonicalizing the path.
> ex include($_GET['page']); or require($_GET['page']); — very common in PHP.
Older PHP apps often use page param to include templates (e.g., index.php?page=home).
* **No canonicalization / whitelist:** There’s no normalization (realpath/canonicalization) and no allowlist restricting which files or directories may be accessed.
* **Insufficient privilege separation:** The application runs with filesystem permissions that allow reading sensitive files.
* **Lack of output filtering:** File contents are returned to the user directly without checks, so even sensitive files (or the lab flag) are exposed.

In short: the server trusted user input for selecting files and lacked server-side checks to enforce allowed paths.

---

## 3) How I exploited it 

### Realistic discovery method

1. Try simple traversal payloads in the parameter to test whether `..` sequence is interpreted by the server:

   * `../`
   * `../../`
   * `../../../`
     Increase the number of `../` until you escape the webroot.
2. i try many files/locations that could contain any sensative data in a linux/unix systems like :
* /etc/shadow
* /etc/gshadow
* /etc/ssh/ssh_host_*
* .ssh/id_rsa
* /etc/ssl/private/
* /etc/mysql/my.cnf, /etc/postgresql/*
* config.php, settings.php
* /proc/kcore, /dev/mem, /dev/kmem
* then /etc/passwd reveals the flag.
---

## 4) What the impact could be

* **Sensitive file disclosure:** attackers can read system files (e.g., `/etc/passwd`), configuration files (`config.php`, `.env`), private keys, or application data.
* **Credential exposure:** files may contain credentials, API keys, or DB connection strings — leading to full system compromise.
* **Local file inclusion / code execution:** in some setups, traversal may lead to inclusion of executable code (LFI → RCE) if the application executes loaded content.
* **Data theft and pivoting:** reading credentials or keys lets attackers move laterally and escalate privileges.
* **High severity:** Path traversal is typically **High to Critical** depending on file access and server privileges.

---

## 5) How to fix it (concrete patches & recommendations)

### Core principles

1. **Never use raw user input as a filepath.**
2. **Whitelist** allowed files or directories; **deny by default**.
3. **Canonicalize** and validate paths before using them.
4. Run the application with **least privilege**—it should not have access to sensitive filesystem areas.


