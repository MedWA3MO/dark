
# Vulnerability: Survey input range bypass (client-side constraint bypass)

**Target page:** `http://localhost:8080/index.php?page=survey`
**Proof-of-concept (POC) request that returned the flag:**

```bash
curl -s 'http://localhost:8080/index.php?page=survey' --data 'sujet=2&valeur=770'
```

---

## 1) What the vulnerability is (short)

The survey form uses a **select input** limited to values `1`–`10` in the UI, but the server does **not validate** that the submitted `valeur` is within that range. By sending a crafted POST with `valeur=770` (outside the allowed UI range), the server accepted it and returned sensitive data (the flag).

**Name:** Client-side constraint bypass / missing server-side input validation.

---

## 2) OWASP Top 10 (2021) classification — which item(s) and why

**Primary classification: A04 — Insecure Design**

* *Why:* The problem stems from a design/logic gap: the application relies on client-side UI controls (a select list) to constrain valid input but lacks a server-side design that enforces business rules (allowed value range). This is an example of insecure design where expected validation logic is missing from the server side.

---

## 3) Why it exists (root cause)

* The developer relied on **client-side controls** (`<select>` element) to limit possible values. Client-side controls are for UX only and can be modified by an attacker (DevTools, proxy, curl).
* **No server-side validation** enforces the allowed range or validates the `sujet`/`valeur` pair.
* The application probably treats `valeur` as a regular parameter in some logic path that returns special content when unusual values are given — and that logic was not hardened.

---

## 4) How you exploited it (step-by-step, minimal)

1. Open the survey page in a browser and note the `Grade`/`valeur` is a `<select>` limited to `1..10`.
2. Instead of using the UI, craft a POST request that sets `valeur` to any value greater than 10 for ex `770`:

   ```bash
   curl -s 'http://localhost:8080/index.php?page=survey' --data 'sujet=2&valeur=770'
   ```
3. The server accepted the request and returned the flag (sensitive content) in the response — demonstrating that client-side limits were ineffective.

**PoC evidence:** include the exact curl above and the HTTP response showing the flag (capture body or screenshot).

---

## 5) What the impact could be

* **Sensitive data disclosure:** returning flags or other secrets.
* **Business-logic abuse:** attackers can trigger behavior not intended by the app (special messages, debug paths, or admin flows).
* **Data integrity & trust failures:** invalid inputs may cause incorrect processing or reveal internal state.
* **Potential pivoting:** if out-of-range values can access other flows (admin, debug), attacker could escalate further.

**Severity:** Medium → High depending on what the server reveals for out-of-range inputs. In your lab it revealed a flag (high impact for CTF).

---

## 6) How to fix it

**Core rule:** Enforce all input validation and business logic rules **on the server side**. Client-side controls are only for usability.

* Minimal server-side validation (concept)

* Check that `valeur` is numeric and within allowed range:
