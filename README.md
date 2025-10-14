Darkly is one of the **42 cybersecurity projects** where you explore a vulnerable web application inside a virtual machine and **hunt flags** by exploiting its weaknesses. This README will help you (and others) get started, from downloading the ISO to accessing the web app and troubleshooting common issues.

---

## 📥 1. Download the ISO

* Go to your **42 Intra** (intranet).
* Navigate to the **Darkly project page**.
* Download the file:

  ```
  Darkly_i386.iso
  ```

  *(it’s usually provided in the resources section)*

---

## 💻 2. Run the ISO in QEMU (no VirtualBox required)

If you don’t want to use VirtualBox, you can run it directly with **QEMU**.

Install QEMU:

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install qemu-system -y

# Arch
sudo pacman -S qemu-full

# Mac (Homebrew)
brew install qemu
```

Then boot Darkly:

```bash
qemu-system-x86_64 -cdrom Darkly_i386.iso -m 1024 \
  -nic user,hostfwd=tcp::8080-:80
```

If you're using your own laptop, run it as root: 

```bash
sudo qemu-system-x86_64 -cdrom Darkly_i386.iso -m 1024 -nic user,hostfwd=tcp::8080-:80
```

Explanation:

* `-cdrom Darkly_i386.iso` → load the ISO as a virtual CD-ROM
* `-m 1024` → allocate 1GB RAM
* `-nic user,hostfwd=tcp::8080-:80` → forward host port `8080` → VM port `80`

---

## 🌐 3. Access the Darkly Website

Once the VM boots:

* Open your browser and go to:
  👉 `http://localhost:8080`

This will show the vulnerable web application hosted inside Darkly.

---

## 🐭 Troubleshooting: QEMU grabs the mouse pointer (Linux host)

**Problem:** When QEMU launches, it captures (grabs) your mouse pointer and you cannot move the host cursor or switch out of the VM window easily.

**Quick fix (GUI QEMU/virt-manager / or QEMU window shortcuts on many distros):**

1. While the QEMU window is focused, press `Alt + v`.
2. Use the arrow keys to move down to the `Grab on hover` menu item.
3. Press `Enter` to **uncheck** `Grab on hover`.

After that, the VM window will no longer automatically grab the mouse pointer when you hover it, and you can move the cursor freely between your host and the VM.

**Alternative (general QEMU behavior):**

* Press the QEMU release key combination (commonly `Ctrl + Alt`) to release mouse/keyboard capture. This depends on your environment and QEMU frontend.

---

## 🎯 4. The Goal – Hunt the Flags

Your mission is to:

* Explore the website.
* Find vulnerabilities (SQLi, XSS, weak auth, etc.).
* Collect **all the flags** hidden across the site.

⚠️ Remember: this environment is **intentionally vulnerable**. Never expose it to the internet!

---

## 🛠️ 5. Useful Notes & Extras

* If you prefer **VirtualBox**, just create a new VM and use `Darkly_i386.iso` as the boot disk.
* To forward **multiple ports** in QEMU (like SSH or HTTPS):

  ```bash
  qemu-system-x86_64 -cdrom Darkly_i386.iso -m 1024 \
    -nic user,hostfwd=tcp::8080-:80,hostfwd=tcp::2222-:22,hostfwd=tcp::8443-:443
  ```
* To stop the VM, close the terminal or press <kbd>Ctrl</kbd> + <kbd>C</kbd> in the process terminal.

---

# [🛡️ OWASP Top 10 — 2021 Summary](https://owasp.org/www-project-top-ten/)

The OWASP Top 10 is a standard awareness document for developers and web application security. It represents a broad consensus about the most critical security risks to web applications:

---

## [🔢 A01:2021 — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
> **Moved up** from the fifth position.  
94% of applications were tested for some form of broken access control.  
The **34 CWEs** mapped to this category had more occurrences than any other.  

---

## [🔐 A02:2021 — Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
> Previously **Sensitive Data Exposure**.  
This category focuses on **cryptographic weaknesses** leading to sensitive data exposure or system compromise.  
It moves up one position to **#2**.  

---

## [💉 A03:2021 — Injection](https://owasp.org/Top10/A03_2021-Injection/)
> **Slides down** to the third position.  
94% of applications were tested for some form of injection.  
Now includes **Cross-Site Scripting (XSS)** under this category.  

---

## [🧠 A04:2021 — Insecure Design](https://owasp.org/Top10/A04_2021-Insecure_Design/)
> 🆕 **New category for 2021.**  
Focuses on **design flaws** and the importance of **threat modeling**, **secure design patterns**, and **reference architectures** to “move left” in the SDLC.

---

## [⚙️ A05:2021 — Security Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
> Moved up from **#6**.  
90% of applications were tested for some form of misconfiguration.  
The former **XML External Entities (XXE)** category is now part of this.  

---

## 🧩 [A06:2021 — Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)
> Previously **Using Components with Known Vulnerabilities**.  
Now ranked higher, moving from **#9** in 2017.  
This remains a persistent issue with **no direct CVE mapping**, but weighted for exploit and impact (5.0).

---

## [👤 A07:2021 — Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
> Previously **Broken Authentication**, now includes identification-related CWEs.  
Slides down from **#2** but remains critical due to authentication complexity and implementation risks.

---

## [🧬 A08:2021 — Software and Data Integrity Failures](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures)
> 🆕 **New for 2021.**  
Focuses on assumptions around **software updates**, **critical data**, and **CI/CD pipelines** without verifying integrity.  
Includes **Insecure Deserialization** from 2017.

---

## [📜 A09:2021 — Security Logging and Monitoring Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures)
> Previously **Insufficient Logging & Monitoring**.  
Now broader, reflecting real-world **visibility, alerting, and forensics challenges**.  
Moves up from **#10** due to community emphasis.

---

## [🌐 A10:2021 — Server-Side Request Forgery (SSRF)](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/)
> 🆕 **Added from community survey (#1)**.  
While still rare in data, it poses **high impact and exploit potential**, representing a strong community-driven inclusion.

---

### 📚 References
- [OWASP Top 10 – 2021 Official Report](https://owasp.org/Top10/)
- [Common Weakness Enumeration (CWE)](https://cwe.mitre.org/)
- [CVE/CVSS Scoring System](https://www.first.org/cvss/)

---

> 💡 **Pro Tip:** Understanding these categories helps developers prioritize secure design and coding practices across the entire software lifecycle.


---
## 📚 Resources
* [The OWASP official website]( https://owasp.org/)
* [QEMU Documentation](https://www.qemu.org/docs/)
* [42 Intra – Darkly Project Page](https://projects.intra.42.fr/projects/42cursus-darkly)

---
