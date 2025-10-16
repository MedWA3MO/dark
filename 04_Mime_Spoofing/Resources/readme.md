# File Upload Bypass Vulnerability

## 1. How did I spot the vulnerability?

While exploring the upload page at:

```
http://localhost:8080/index.php?page=upload
```

I noticed that the form only allows uploading files with `.jpg` or `.jpeg` extensions.

However, after checking the behavior:

1. The form uses **JavaScript** to block empty uploads but doesn’t inspect the actual file content.
2. The backend **only checks file extensions**, not the real MIME type or file structure.
3. This means that if we disguise a PHP file as a JPEG, the server might still accept it.

---

## 2. How did I test the vulnerability?

First, I created a simple PHP test file:

```bash
echo '<?php echo "hello"; ?>' > test.php
```

Then, I used **cURL** to upload it by **spoofing the Content-Type**:

```bash
curl "http://localhost:8080/index.php?page=upload" \
  -F "Upload=Upload" \
  -F "uploaded=@test.php;type=image/jpeg"  | grep "flag"
```

### Explanation of each part:

* `curl` — command-line tool to make web requests
* `"http://localhost:8080/index.php?page=upload"` — target upload endpoint
* `-F "Upload=Upload"` — mimics the form button named `Upload`
* `-F "uploaded=@test.php;type=image/jpeg"` — sends the file `test.php` pretending it’s a JPEG
* `-F "MAX_FILE_SIZE=100000"` — sets the maximum allowed size field used by the form
* `| grep "flag"` — searches the response for the word “flag” (typical in CTFs)

This worked because the server trusted the `Content-Type` header we sent manually.
Browsers, on the other hand, **don’t let you override Content-Type or form fields freely**, which is why **this test must be done via cURL or a similar tool**, not from a normal webpage.

---

## 3. What is the vulnerability?

**File Upload Bypass** — the application allows non-image files (like `.php`) to be uploaded by trusting the file extension or spoofed MIME type instead of validating the actual file content.

---

## 4. Why does it exist (the security flaw)?

* The server checks only **file extensions**, not the binary file signature.
* There’s **no server-side validation** using libraries like `fileinfo`.
* Uploaded files are stored in an **executable directory**, allowing attackers to run code.

---

## 5. What could the impact be?

* **Remote Code Execution (RCE):** Upload and execute arbitrary PHP code on the server
* **Data Theft:** Read or exfiltrate sensitive files
* **Full System Compromise:** Modify or delete data, escalate privileges, or take over the host

---

## 6. How to fix it (patch)?

1. **Validate actual file content**, not just extensions.
2. **Use the `fileinfo` PHP library** to check MIME types properly.
3. **Re-encode uploaded images** server-side before saving.
4. **Store uploads outside the webroot** (non-executable directory).
5. **Apply a strict Content Security Policy (CSP)**.

---

## 7. Vulnerability classification (OWASP)

**A01 - Broken Access Control**
*(because the system fails to properly restrict what files can be uploaded and executed)*

---

