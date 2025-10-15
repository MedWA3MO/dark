# Brute Force Attack Vulnerability

## 1. How did i spot the Vulnerability?

- I saw this signing page on this link:

-  http://localhost:8080/index.php?page=signin

- I started testing different usernames and different passwords over and over again and I noticed that there is no protection for how many times you can try.

- I noticed also that the website always redirects you to this link when you click on login:

- (here when trying test as username, and test as password)

- http://localhost:8080/index.php?page=signin&username=test&password=test&Login=Login#

- So I installed Hydra. (specifically THC-Hydra) is a popular penetration testing tool used for password brute-forcing and credential attacks.

- And I also created a list of popular usernames on usernames.txt and a list of popular passwords on passwords.txt.

- Then I ran this command:

```bash
hydra -L usernames.txt -P passwords.txt localhost -s 8080 http-get-form "/index.php:page=signin&username=^USER^&password=^PASS^&Login=Login:F=images/WrongAnswer.gif"
```

Hydra found some username and a password which is a vulnerability. Once you enter them you get the flag.

## 2. What is the vulnerability?

Brute Force Attack - the application allows unlimited login attempts without any rate limiting or account lockout mechanisms.

## 3. Why does it exist (the security flaw)?

The application lacks:
- Rate limiting on login attempts
- Account lockout after failed attempts
- CAPTCHA or challenge-response mechanisms


## 4. What could the impact be?

- Unauthorized account access through automated credential attacks
- Complete account takeover
- Data breach and exposure of sensitive information


## 5. How to fix it (patch)?

- Implement rate limiting (e.g., max 5 attempts per minute)
- Add account lockout after consecutive failed attempts (e.g., lock for 15 minutes after 5 failures)
- Implement CAPTCHA after 3 failed attempts

## 6. Vulnerability classification (OWASP)?

**A07 - Identification and Authentication Failures**