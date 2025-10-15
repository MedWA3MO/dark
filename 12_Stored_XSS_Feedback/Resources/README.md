# XSS Vulnerability Testing Report

## 1. How did i spot the Vulnerability?

I went to the feedback page: `http://localhost:8080/index.php?page=feedback`

It's a feedback/guestbook form where you can see other people's submissions including mine.

## Testing Phase 1: Character Validation

So let's see what characters are allowed?

Let's start with the field Comment...

**Test 1:**
- Name: `test`
- Comment: `Hello @#$%^&*()`
- Result: Looks normal

**Test 2:**
- Name: `test`
- Comment: `Hello <> [] {}`
- Result: Looks normal but `<>` are not displayed!?

If `<>` are allowed...

## Testing Phase 2: HTML Injection

Let's try to inject HTML code.

**Test 3:**
- Name: `test`
- Comment: `<b>bold</b>`
- Result: I see the text "bold" but the bold style was not applied.

**Test 4:**
- Name: `test`
- Comment: `<h1 style="color: #ffeb3b;">HTML</h1>`
- Result: I see the same, no HTML styling applied.

Seems like the backend is protecting HTML code.

## Testing Phase 3: JavaScript Injection

Let's try injecting some JS code:

**Test 5:**
- Name: `test`
- Comment: `<script>alert('test')</script>`
- Result: I see only this text `alert(\'test\')` and `<script>` with `</script>` are removed.

Looks like the backend is parsing JS code when injected...

## Testing Phase 4: HTML Elements with JavaScript Events

But what if we inject HTML Elements That Execute JavaScript?

**Test 6:**
- Name: `test`
- Comment: `<svg onload=alert(1)>`
- Result: I see no alert and comment is empty...

I also tested these codes in comment:
```html
<svg/onload=alert(1)>
<svg/onload=alert('XSS')>
<svg/onload=alert`1`>
```

Seems like HTML with JS is protected well.

## Testing Phase 5: Name Field Testing

Ok, how about the Name field? It takes up to 10 chars.

If you test with a short HTML code like:

**Test 7:**
- Name: `<h1>A</h1>`
- Message: `test`
- Result: **We get the flag!** Seems like the field Name is not well protected against XSS.

I tried to reverse:

**Test 8:**
- Name: `test`
- Comment: `<h1>A</h1>`
- Result: **I get the flag too!** Well, seems like the field Comment is not well protected too.

---

## 2. What is the vulnerability?

Stored Cross-Site Scripting (XSS) - the application accepts user input through the feedback form but fails to properly sanitize or encode it before storing and displaying it to other users.

## 3. Why does it exist (the security flaw)?

The application uses a blacklist approach wthat blocks obvious patterns like `<script>` tags, but can be bypassed with alternative HTML tags (like `<h1>`, `<svg>`) containing JavaScript event handlers. 

## 4. What could the impact be?

- Session hijacking by stealing login cookies
- stealing other users senstice data , by applying you injected code in this session.


## 5. How to fix it (patch)?

- Implement proper output encoding on ALL user-generated content .
- Convert special characters like `<` to `&lt;` so browsers treat them as text, not executable code


## 6. Vulnerability classification (OWASP)?

**A03 - Injection** (specifically Stored/Persistent Cross-Site Scripting)