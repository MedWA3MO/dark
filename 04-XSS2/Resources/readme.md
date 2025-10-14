# Vulnerability: keyword-trigger on feedback page (information disclosure)

**Target page:** `http://localhost:8080/index.php?page=feedback`
**Short finding:** Submitting feedback that contains the substring `script` (or an attempted script) caused the application to reveal the flag. The server appears to treat the presence of that keyword as a special trigger rather than properly sanitizing or handling user input.

---

## 1) What the vulnerability is (OWASP classification)

**Vulnerability name:** Keyword-trigger / backdoor-like logic that reveals secrets when certain input is present.

**OWASP Top 10 (2021) classification:**

* **Primary:** **A04 — Insecure Design** — the application contains a design decision/feature that treats specific user-controlled input (`script`) as a special event and returns sensitive data. This is a logic/design flaw.
* **Secondary:** **A05 — Security Misconfiguration** — likely a leftover debug/backdoor or misconfiguration where special-case logic was left enabled in a deployed app.

(Although `script` suggests XSS, this issue is not a vanilla XSS: it is an application-side keyword trigger that causes information disclosure, so A04/A05 are the best fits.)

---

## 2) Why it exists (root cause / security flaw)

A realistic technical explanation for how this arose:

* During development, the team added a **simple detector** to identify attempted script injection in feedback (e.g., to flag abuse or attempts at XSS).
* Instead of **logging** or safely handling that detection server-side, the code implemented a **special-case response**: when the detector sees the substring `script` (or a pattern matching `<script`), it returns a “challenge” or test response — in this lab that response includes a flag.
* The detector is overly simplistic (substring match), applied to **user-supplied content**, and the special-case response remained enabled in the deployed environment.
* In short: **a debug/monitoring mechanism (or naive XSS detector) was misused to trigger a privileged response based on attacker-controlled input.**

Why this is bad:

* User input must never be used as a direct trigger for privileged behavior (revealing secrets, flags, or admin responses).
* Keyword-based detectors are error-prone and can be trivially triggered by an attacker.

---

## 3) How I exploited it (step-by-step)

A realistic, reproducible discovery path (tools + reasoning):

1. **Recon / curious testing:** When interacting with the feedback form, a tester typically tries benign inputs and then small variations (this is normal fuzzing). Example test values: `hello`, `<b>test</b>`, `<script>alert(1)</script>`, `script`, `ScRiPt`.
2. **Observation:** While trying an attempted script payload or even just the word `script` the server responded differently (the response contained extra content).
3. **Result:** The server returned the flag when the keyword was present.

---

## 4) What the impact could be

* **Information disclosure:** Revealing flags, secrets, or internal diagnostics to unprivileged users.
* **Proof-of-concept backdoor:** Any keyword-based backdoor can be abused to reveal additional internal behavior or secrets.
* **Recon from unauthenticated users:** Attackers can probe freely to discover more hidden triggers or behavior.
* **Potential chaining:** If the trigger reveals internal data (config values, tokens), it can be combined with other vulnerabilities for escalation.

**Severity:** High for any production system if sensitive information can be disclosed based on user input. For lab/CTF this is a direct flag disclosure.

---

## 5) How to fix it (patch / concrete recommendations)

### Immediate fixes

1. **Remove special-case trigger logic** that returns secrets or flags when certain substrings are present. There should be no privileged response based on raw user input.
2. **Replace the detector behavior**: if you need to detect attempted script tags, log the event server-side and alert — do **not** return sensitive content or special responses. Example:

   * On detection: `log("XSS attempt from IP ...", payload)` and return a neutral, sanitized page.

### Input handling & XSS protection

3. **Treat user input as data, not code**:

   * Always HTML-escape user-supplied text before reflecting it into pages (`htmlspecialchars()` in PHP, appropriate templating escaping in frameworks).
4. **Implement proper XSS protections**:

   * Use Content Security Policy (CSP) to mitigate script execution.
   * Set `X-Content-Type-Options: nosniff` and other security headers.
5. **Avoid keyword-based logic for privileged behavior**:

   * Never gate sensitive operations on the presence or absence of specific strings in user input.

