# Open Redirect Vulnerability
<!-- 
## What is this vulnerability?
An Open Redirect vulnerability occurs when a web application redirects users to external URLs without proper validation. The application trusts user input to determine the destination URL, allowing attackers to redirect users to malicious websites while maintaining the appearance of legitimacy through the original trusted domain. -->



## How to spot it technically

### Visual Inspection:
- When inspecting the page, I noticed that clicking on social media icons takes you to something like: `http://localhost:8080/index.php?page=redirect&site=facebook`

- This means our site has some kind of table of links where it redirects based on the `site` parameter.

- But what if I test with something of my own, like:

  `http://localhost:8080/index.php?page=redirect&site=test`

- Tarra! We get the flag, meaning that our site is not optimized to block suspicious redirections.

## Why is this dangerous?

### Attack Scenarios:

   - Victims see the trusted domain (http://localhost:8080/index.php) but get redirected to malicious sites



---

### What the Vulnerability Is
An **Open Redirect** where the application accepts user-controlled input (`site` parameter) to determine redirect destinations without validation, allowing attackers to redirect users from a trusted domain to malicious sites.

### Why It Exists (The Security Flaw)
- **No Input Validation**: The `site` parameter is not validated before redirecting
- **Missing Whitelist**: No list of approved redirect destinations


### What the Impact Could Be
- **Phishing Attacks**: Redirect users to fake login pages that steal credentials
- **Malware Distribution**: Redirect t```o sites hosting malware
- **Brand Reputation Damage**: Company domain used for attacks

### How to Fix It (Patch)
**Primary Defense - Whitelist:**


## Vulnerability Classification


**OWASP Classification:** A01:2021 - Broken Access Control


