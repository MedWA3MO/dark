# How I found the flag in `.hidden` — step-by-step

## TL;DR

1. Manually discovered the `.hidden` directory on the local web server.
2. Explored it by hand and found many nested folders with `README` files deep inside; each README often said "Tu veux de l'aide ? Moi aussi !".
3. To avoid manual crawling, used `wget` to fetch README/flag-like files from all subfolders.
4. Searched downloaded files with `grep` for keywords `flag`, `encrypt`, and `lowercase`.
5. Found the flag in `README.15794`:

```
Hey, here is your flag : d5eec3ec36cf80dce44a896f961c1831a05526ec215693c8f2c39543497d4466
```

---

## Full steps (what I did, in order)

### 1) Find the `.hidden` directory

* Open a browser or use `curl` to visit `http://localhost:8080/` and look for interesting links. I found `/.hidden/` in the index.

### 2) Explore manually (what this looks like)

* Clicking into `.hidden/` shows many folders with random-looking names. I opened a few by hand and navigated deeper (enter folder → back → enter another folder). After repeating this a few times I noticed a pattern: most branches contained a `README` that read "Tu veux de l'aide ? Moi aussi !" and no flag. That suggested brute-force crawling would be faster.

### 3) Automate fetching README/flag-like files with `wget`

Instead of clicking each folder, I used a controlled `wget` approach to download candidate files.

#### Command I used (single line):

```bash
# run from a folder where you want the files saved         
        wget -r -np -nd -e robots=off -A "README*,README,flag*,Flag*,*.txt" http://localhost:8080/.hidden/
```

**Why I used this exact command** (detailed explanation):

* `wget` — a command-line tool that downloads files from web servers.

**Options and why they matter:**

* `-r` (recursive): follow links on pages to find files. We must follow the index links to reach subfolders.
* `-np` (no-parent): prevents `wget` from following links back to parent directories. Keeps the crawl inside `.hidden/`.
* `-nd` (no-directories): save all files to the current local directory rather than recreating the remote directory tree. This keeps filenames simple and easy to search locally.
* `-e robots=off`: ignore `robots.txt` rules. In local labs this helps fetch files that might otherwise be hidden by robots rules (safe for local testing). Use carefully on remote targets.
* `-A "README*,README,flag*,Flag*,*.txt"` (accept list): only download files whose names match these patterns. This prevents `wget` from saving every single asset (images, css) — it only saves likely README/flag files and `.txt` files where the flag might be.

---

### 4) Search the downloaded files with `grep`

After the `wget` run, I used `grep` to quickly find any README or text file that mentions likely clue words.

#### Command I used:

```bash
grep -inE "flag|encrypt|lowercase" * 2>/dev/null
```

**Why and what each part does:**

* `grep` — search for text inside files.
* `-i` — case-insensitive search (matches `Flag` and `flag`).
* `-n` — show the line number where the match occurred (helps locate content in longer files).
* `-E` — enable extended regular expression syntax so `|` works as OR (search for any of the words).
* `"flag|encrypt|lowercase"` — the pattern: match any occurrence of `flag`, `encrypt`, or `lowercase`.
* `*` — search all files in the current folder (the files `wget` saved).
* `2>/dev/null` — hide error messages (e.g., from grep trying to read non-text/binary files), which keeps the output clean.

This printed a line identifying `README.15794` with the flag.

---

### 5) Read the matching README to capture the flag

I then opened the file to confirm the flag contents:

```bash
cat README.15794
# or
less README.15794
```

The README contained:

```
Hey, here is your flag : d5eec3ec36cf80dce44a896f961c1831a05526ec215693c8f2c39543497d4466
```

Record that value (and screenshot or save the response) for your report.

---

## Notes & good practices

* Always do this only on systems you own or are explicitly allowed to test (this was a local purposeful learning lab).
* If you need to crawl deeper or want to try alternate README names (like `README.md`, `readme.txt`), add those patterns to the `-A` list or adjust your fetch loop to try more names. Example: `-A "README*,README,readme.txt,README.md,flag*,Flag*,*.txt"`.
* For reproducibility include the exact commands and timestamps in your report so others can verify your steps.

d5eec3ec36cf80dce44a896f961c1831a05526ec215693c8f2c39543497d4466



Below is a concise, well-structured write-up you can drop into a `README.md` (or include in your report) that answers the five questions for the `.hidden` directory vulnerability you discovered. It includes the short PoC commands you used and clear mitigation guidance.

---

# README — Discovery: exposed `.hidden` directory (file enumeration)

**Finding:** public directory index (`http://localhost:8080/.hidden/`) contained many nested folders and `README` files; one README contained the flag:

```
Hey, here is your flag : d5eec3ec36cf80dce44a896f961c1831a05526ec215693c8f2c39543497d4466
```

Below I answer the five requested questions about this issue.

---

## 1) What the vulnerability is (classification, OWASP)

**Vulnerability name:** Directory indexing / exposed files (information disclosure).

**OWASP classification:**

* **Primary:** **Security Misconfiguration** (OWASP Top 10 — A05 or the equivalent depending on the year): the web server is exposing internal folders and files through an index.
* **Secondary:** **Sensitive Data Exposure** (A03) when the exposed files contain secrets/flags.
  (You may also mention **Broken Access Control** if files should have been protected but were not.)

**Short description:** The web server allows directory listing and stores sensitive files inside a publicly accessible path. Anyone who browses to `.hidden/` can enumerate files and retrieve secret data.

---

## 2) Why it exists (the root cause / security flaw)

* **Directory listing enabled:** The web server is configured to show directory contents when no index file exists (e.g., `Options +Indexes` or equivalent).
* **Secrets stored under webroot:** Files containing sensitive information (flags, notes) were placed in a folder served by the webserver instead of a protected location.
* **False sense of hiding:** A `robots.txt` or random folder names were used to “hide” content, but `robots.txt` is advisory and *does not* prevent access. Security by obscurity (random names) is not protection.
* **No access control:** No authentication or ACLs protect `.hidden/` or its subfolders.

---

## 3) How you exploited it (step-by-step, minimal, reproducible)

**Manual reconnaissance**

1. Visited the site index: `http://localhost:8080/`
2. Noticed a link to `/.hidden/` and opened it. Directory index shows many subfolders.

**Automated enumeration (safe local PoC)**
To avoid manually clicking many nested folders, I downloaded likely candidate files and searched them for clues:

```bash
# 1) Recursively fetch README and text-like files from the .hidden index
wget -r -l1 -np -nd -e robots=off \
  -A "README*,README,readme.txt,README.md,flag*,Flag*,*.txt" \
  "http://localhost:8080/.hidden/"

# 2) Search downloaded files for likely keywords
grep -inE "flag|encrypt|lowercase" * 2>/dev/null
```

* `-l1` limits recursion to immediate children of `.hidden/` (quick & safe).
* `-e robots=off` was necessary because `robots.txt` included `Disallow: /.hidden` (robots.txt is not a security mechanism).
* `grep` located `README.15794` containing the flag string.

**Evidence:** `cat README.15794` showed the exact flag line above.

> **Note:** Only run these commands on systems you own or are authorized to test.

---

## 4) What the impact could be

* **Sensitive information disclosure:** Flags, secrets, credentials, or internal notes are revealed.
* **Escalation and pivoting:** If files contain credentials or tokens, an attacker could gain deeper access.
* **Reputation and compliance damage:** Exposed confidential data may violate policy or leak private info.
* **Automated discovery at scale:** Attackers and scanners routinely look for open indexes — risk is high if secrets are present.

**Severity:** Medium → Critical depending on what the exposed files contain. In your lab, the impact is the flag disclosure (CTF-relevant); in production, it could be far worse.

---

## 5) How to fix it (patch / concrete steps)

### Immediate remediation (quick fixes)

1. **Remove sensitive files from webroot** — move them outside the publicly served directory.

   * e.g., move `/var/www/html/.hidden/` contents to `/var/secrets/` or delete if not needed.

2. **Disable directory listing** on the web server:

   * **Apache (global or in site config / `.htaccess`):**

     ```apache
     Options -Indexes
     ```
   * **Nginx:**

     ```nginx
     location / {
       autoindex off;
     }
     ```

3. **Restrict access to the directory** (if the directory must remain on the server):

   * Apache `.htaccess`:

     ```
     <Directory "/var/www/html/.hidden">
       Require all denied
     </Directory>
     ```
   * Nginx:

     ```nginx
     location /.hidden/ {
       deny all;
       return 403;
     }
     ```
   * Or protect with HTTP auth if needed for legitimate users.

4. **Remove sensitive lines from `robots.txt`** that claim to “hide” directories — `robots.txt` is not a security measure. (Either remove `Disallow: /.hidden` or keep it only if you understand it’s not protective. But don’t rely on it to hide secrets.)

### Recommended long-term hardening

* **Never store secrets in web-accessible directories.** Store configs, keys, or secret files outside `DocumentRoot`.
* **Use principle of least privilege:** files & directories should have minimal permissions (owner-only read where appropriate).
* **Audit & scan:** periodic scans for exposed files (automated checks for world-readable files under webroot).
* **Logging & alerting:** monitor for unexpected directory listing access patterns.
* **Review deployment processes:** ensure CI/CD or developers don’t accidentally deploy secrets to webroot.

### Example: move files and block access (quick commands)

```bash
# move the directory out of webroot
mv /var/www/html/.hidden /var/secrets/.hidden_backups

# block access (nginx example) — include in nginx site config and reload
# location /.hidden/ { deny all; return 403; }
sudo systemctl reload nginx
```

---

## Extra notes for reporting

* **Repro steps:** include the exact URL (`http://localhost:8080/.hidden/`), the wget command used, and the filename where you found the flag (`README.15794`). Add screenshots or `curl -I`/response if possible.
* **Responsible disclosure:** For a real target, do not exfiltrate or publish secrets — contact the owner with proof and remediation steps.
* **For the lab:** include the remediation notes in your final report and mention that finding the flag was done in a local authorized environment.

---

If you want, I can:

* Create a ready-to-drop `README.md` file in your workspace with this text, or
* Generate an Nginx/Apache snippet you can paste into config to immediately block `.hidden/`. Which do you prefer?
