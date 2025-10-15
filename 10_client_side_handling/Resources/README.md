# Hidden Form Field Manipulation Vulnerability

## 1. How did i spot the Vulnerability?

- I went to the signing page here: http://localhost:8080/index.php?page=signin

- I saw "I forgot my password" link clicking on it will take you - here: http://localhost:8080/index.php?page=recover

After inspecting the page I can see this:

```html
<form action="#" method="POST">
    <input type="hidden" name="mail" value="webmaster@borntosec.com" maxlength="15">
    <input type="submit" name="Submit" value="Submit">
</form>
```

- We can clearly see that this field is hidden from the page.

- When clicking on submit it sends a POST method with webmaster@borntosec.com as a default value.

- Meaning that the website is using a default client-side value without server-side verification.

- But what if we change it?

- We can manipulate the value by changing it in the HTML or by using this command:

```bash
curl 'http://localhost:8080/index.php?page=recover' --data 'mail=test@42.fr&Submit=Submit' | grep flag
```

## 2. What is the vulnerability?

Hidden Form Field Manipulation - the application stores sensitive information (administrator's email) in a hidden form field that can be easily modified by the client.

## 3. Why does it exist (the security flaw)?

The application relies on client-controlled hidden form fields without server-side validation. 

## 4. What could the impact be?

- Password recovery emails redirected to attacker's email address
- Account takeover through compromised password reset functionality


## 5. How to fix it (patch)?

- Never store sensitive data in hidden form fields
- Store administrator email securely in the server-side database
- Retrieve the email server-side during password recovery
- Never expose sensitive information to the client
- Implement proper server-side validation for all form inputs


## 6. Vulnerability classification (OWASP)?

**A04 - Insecure Design**