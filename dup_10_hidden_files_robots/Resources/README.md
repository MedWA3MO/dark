# Information Disclosure via robots.txt

## 1. How did i spot the Vulnerability?

robots.txt is a file that tells search engines and web crawlers which parts of a website they should NOT visit.

When we visit http://localhost:8080/robots.txt

We notice this folder: `Disallow: /.hidden`

Disallow tells the search engine don't index this folder, but it is still accessible.

## Exploitation Process

I downloaded the folder using this command:

```bash
wget -r -l 5 -np -e robots=off http://localhost:8080/.hidden/
```

**Command breakdown:**
- `-r` = Recursive (follow links and download subdirectories)
- `-l 5` = Limit recursion depth to 5 levels
- `-np` = No parent
- `-e robots=off` = Execute command: ignore robots.txt rules

I accessed it using:

```bash
cd localhost:8080/.hidden
```

Then I searched for any file where the term flag was typed in this directory or subdirectories:

```bash
grep -r "flag" .
```

**Command breakdown:**
- `-r` = Recursive (search all files in all subdirectories)

Then we found the flag: `d5eec3ec36cf80dce44a896f961c1831a05526ec215693c8f2c39543497d4466`


## 2. What is the vulnerability?

Information Disclosure through robots.txt misconfiguration - using robots.txt to hide sensitive directories while leaving them publicly accessible.

## 3. Why does it exist (the security flaw)?

Misunderstanding that robots.txt provides security protection when it only serves as a polite suggestion for well-behaved web crawlers. 

## 4. What could the impact be?

- Exposure of sensitive files and directories
- Discovery of hidden admin panels or development files
- Access to backup files, configuration files, or source code


## 5. How to fix it (patch)?

- Never rely on robots.txt for security

## 6. Vulnerability classification (OWASP)?

**A01 - Broken Access Control** and **A05 - Security Misconfiguration**