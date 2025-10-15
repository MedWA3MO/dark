# HTTP Header Manipulation Vulnerability

## 1. How did I spot the Vulnerability?

- In the bottom of each page there's a clickable link called "© BornToSec"
- Clicking on it takes you to a new page
- I inspected the page and saw these comments:

```html
<!--
You must come from : "https://www.nsa.gov/".
-->
```

and 

```html
<!--
Let's use this browser : "ft_bornToSec". It will help you a lot.
-->
```

These comments indicate that the website expects requests to come from `https://www.nsa.gov/` and use `ft_bornToSec` as the browser User-Agent.

I simulated this using curl with the following command:

```bash
curl -H "User-Agent: ft_bornToSec" -H "Referer: https://www.nsa.gov/" "http://localhost:8080/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f" | grep -i flag
```

The flag was successfully retrieved: `f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188`

## 2. What is the vulnerability?

HTTP Header Manipulation (HTTP headers are pieces of information sent between your browser (client) and a website's server with every request and response. )- the application makes access control decisions based on easily forgeable HTTP headers (User-Agent and Referer) that are completely controlled by the client.

## 3. Why does it exist (the security flaw)?

The application trusts client-controlled data for authentication/authorization. 
## 4. What could the impact be?

- Unauthorized access to restricted content and admin panels
- Authentication and authorization bypass
- Access to sensitive business data without proper credentials

## 5. How to fix it (patch)?

**Never use HTTP headers for access control decisions.** Instead:

- Implement proper session-based authentication with server-side validation
- Validate all authentication server-side with proper session management
- Implement session timeouts and lifecycle management

## 6. Vulnerability classification (OWASP)?

**A01 - Broken Access Control**