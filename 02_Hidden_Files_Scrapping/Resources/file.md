# How I found the flag in `.hidden` — step-by-step

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
grep -inE "flag|encrypt" * 2>/dev/null
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



##  What the vulnerability is (classification, OWASP)

**Vulnerability name:** Directory indexing / exposed files (information disclosure).

**OWASP classification:**

* **Primary:** **Security Misconfiguration** (OWASP Top 10 — A05 or the equivalent depending on the year): the web server is exposing internal folders and files through an index.
* **Secondary:** **Sensitive Data Exposure** (A03) when the exposed files contain secrets/flags.
  (You may also mention **Broken Access Control** if files should have been protected but were not.)

**Short description:** The web server allows directory listing and stores sensitive files inside a publicly accessible path. Anyone who browses to `.hidden/` can enumerate files and retrieve secret data.

---

##  Why it exists (the root cause / security flaw)

* **Directory listing enabled:** The web server is configured to show directory contents when no index file exists (e.g., `Options +Indexes` or equivalent).
* **Secrets stored under webroot:** Files containing sensitive information (flags, notes) were placed in a folder served by the webserver instead of a protected location.
* **False sense of hiding:** A `robots.txt` or random folder names were used to “hide” content, but `robots.txt` is advisory and *does not* prevent access. Security by obscurity (random names) is not protection.
* **No access control:** No authentication or ACLs protect `.hidden/` or its subfolders.

---


## How to fix it (patch / concrete steps)

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
