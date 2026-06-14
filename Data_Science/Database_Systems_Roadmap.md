# 🗺️ Database Systems & SQL Optimization: A Learning Guide

> 🛡️ **Cyber_Now Lab**: A structured guide for mastering database architecture and SQL optimization to manage large-scale security logs, normalize network intelligence, and ensure high-performance data retrieval for incident response.


---

## 📋 Table of Contents
> 📚 **Purpose**: Outline the structural flow of the database and SQL learning path.
> 🎯 **Goal**: Allow users to quickly locate specific topics from theory to practical application.

1. [What is a DBMS?](#1-what-is-a-database-management-system)
2. [Intro to SQL & Data](#2-intro-to-sql--data)
3. [Understanding Tables & Relationships](#3-understanding-tables--relationships)
4. [🛠️ Modifying Databases: Read vs Write](#4-modifying-databases-read-vs-write)
5. [🗣️ SQL Basics: CREATE & INSERT](#5-sql-basics-create--insert)
6. [SQL Queries: SELECT, ORDER BY, WHERE](#6-sql-queries-select-order-by-where)
7. [Advanced Filtering: IN, Subqueries, & LIKE](#advanced-filtering-in-subqueries--like)
8. [Aggregating Data: GROUP BY & HAVING](#aggregating-data-group-by--having)
9. [Conditional Logic: The CASE Statement](#conditional-logic-the-case-statement)
10. [JOINing Related Tables](#10-joining-related-tables)
11. [OUTER JOINs](#11-outer-joins)
12. [Self Joins](#12-self-joins)
13. [Combining Multiple Joins](#13-combining-multiple-joins)
14. [Roles in the Ecosystem](#14-roles-in-the-ecosystem)
15. [Tools & Resources](#15-tools--resources)
16. [Changing rows with UPDATE and DELETE](#16-changing-rows-with-update-and-delete)
17. [Altering tables after creation](#17-altering-tables-after-creation)
18. [Database Administration & Safety](#18-database-administration--safety)
19. [Next Steps](#19-next-steps)


---

## 1. What is a DBMS?
> 📚 **Purpose**: Define the role and characteristics of Database Management Systems.
> 🎯 **Goal**: Understand how software manages data storage, retrieval, and integrity.

A **Database Management System (DBMS)** is software that manages databases. It provides functionality for:
- Adding data
- Modifying data
- Querying data
- Fast data retrieval

### 7 Core Characteristics
- **Storage Engine**: Efficient data storage
- **Query Optimizer**: Finds best way to execute queries
- **Transaction Manager**: Ensures data integrity
- **Concurrency Control**: Handles multiple users
- **Backup & Recovery**: Protects against data loss
- **Security**: Protects sensitive data
- **API/Interface**: Connects applications to data

### The Database Development Lifecycle (DBLC)
Building a professional database follows a structured path called the **Database Development Lifecycle**:

1.  **Planning**: Defining the project scope, boundaries, and feasibility.
2.  **Analysis**: Gathering requirements from users and stakeholders.
3.  **Design**: Structuring the data models (Conceptual, Logical, Physical).
4.  **Implementation**: Coding the tables (SQL), loading data, and setting up security.
5.  **Maintenance**: Monitoring performance, backups, and making necessary updates.

### Three Levels of Database Design
Design is broken into three distinct phases to ensure the database meets business needs:

| Design Level | Focus | Characteristics |
|--------------|-------|-----------------|
| **Conceptual** | "The Big Picture" | High-level, platform-independent model of data entities. |
| **Logical** | "Table Mapping" | Maps entities to a specific model (like Relational Tables) without worrying about hardware. |
| **Physical** | "Storage Detail" | Determines the actual storage structures and access paths for a specific DBMS (like PostgreSQL or SQLite). |

---

## 2. Intro to SQL & Data
> 📚 **Purpose**: Introduce SQL as the standard language for interacting with relational databases.
> 🎯 **Goal**: Comprehend the core concepts of tables, rows, and columns in data storage.

> 🌟 **The Golden Rule of Thumb**: Use SQL to clean, filter, and aggregate massive datasets down to a manageable size on the database server. Then, pull that refined dataset into pandas for deep-dive analysis, visualization, and machine learning.

### Why Learn SQL?
- **Every app stores data**: Facebook, apps, banks all use databases
- **Relational databases** store data in **tables** (rows = items, columns = properties)
- **SQL** is the most popular language for querying databases
- You'll be able to understand how apps store data

### Real-World Examples
- **Khan Academy**: Stores user data, badges, progress
- **Facebook**: Stores user profiles, friend connections, posts
- **Bank of America**: Stores account balances, transactions

### Relational Database Concepts
- **Tables**: Data organized in rows and columns
- **Relationships**: Link tables together (e.g., users ↔ badges)
- **Efficient Storage**: Avoid repeating data
- **Unique IDs**: Primary keys identify each row

---

## 3. Understanding Tables & Relationships
> 📚 **Purpose**: Explore how data is structured and linked across different tables.
> 🎯 **Goal**: Master primary keys, foreign keys, and normalization to ensure data consistency.

### 3.1 Primary Keys (PK)
A primary key is a field (or set of fields) that uniquely identifies each record in a table.
- **Entity Integrity Rule**: Every table must have a primary key. Values must be **unique** and **NOT NULL**.
- **Characteristics**: A table can have only one primary key. It ensures every record can be identified and prevents duplicates.

### 3.2 Foreign Keys (FK)
A foreign key is a field in one table that refers to the primary key in another table, creating a link between them.
- **Parent Table**: The table containing the referenced primary key.
- **Child Table**: The table containing the foreign key.
- **Characteristics**: Unlike primary keys, foreign keys **can** contain duplicates (e.g., many students in one class) and **can** be NULL if the relationship is optional.

### 3.3 Composite Keys
A primary key that consists of **two or more columns** that together uniquely identify a row. These are commonly used in "junction" tables.

```sql
-- Formal Data Structure Examples
CREATE TABLE users (
    id INTEGER PRIMARY KEY, -- Primary Key
    name TEXT
);

CREATE TABLE badges (
    id INTEGER PRIMARY KEY, -- Primary Key
    name TEXT
);

-- Junction Table for many-to-many relationship
CREATE TABLE user_badges (
    user_id INTEGER,
    badge_id INTEGER,
    earned_at TEXT,
    -- Composite Key: combination of user and badge must be unique
    PRIMARY KEY (user_id, badge_id), 
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (badge_id) REFERENCES badges(id)
);
```

### 3.4 Referential Integrity
A system of rules used by a DBMS to ensure that relationships between records remain valid and consistent.

| Rule Type | Action |
|-----------|--------|
| **Insertion** | Cannot add a Foreign Key value if it doesn't exist in the Parent Table's Primary Key. |
| **Deletion** | Cannot delete a record from a Parent Table if matching records exist in a Child Table (prevents "orphan" records). |
| **Update** | Cannot change a Primary Key value in a Parent Table if it has related records in a Child Table. |

**Maintenance (Cascading)**:
- **Cascade Update**: If you change a PK in the parent table, the DBMS automatically updates the FK in all related child records.
- **Cascade Delete**: If you delete a record in the parent table, the DBMS automatically deletes all related child records.

### 3.5 Why Unique IDs Matter
- **Identify rows**: Find specific records to update/delete.
- **Avoid dependencies**: Don't rely on changing columns (like names).
- **Standard practice**: `id` column first, declared as `INTEGER PRIMARY KEY`.

### 3.6 Table Relationships
Relationships are associations between tables, categorized by **connectivity** and **cardinality**. In professional database design, these are often visualized using **Crow's Foot** notation.

- **One-to-One (1:1)**: A single record in Table A is related to exactly one record in Table B.
    - *Example*: A **Manager** and a **Department**. (One manager runs one department; one department is managed by one person).
- **One-to-Many (1:M)**: A single record in Table A is related to multiple records in Table B. This is the most common relationship.
    - *Example*: A **Painter** and **Paintings**. (One painter can create many paintings, but each painting is typically credited to one painter).
- **Many-to-Many (M:N)**: Multiple records in Table A are related to multiple records in Table B.
    - *Example*: **Students** and **Classes**. (One student takes many classes; one class contains many students).
    - **🔑 The Junction Table Resolution**: Relational databases (SQL) cannot store M:N relationships directly. They must be resolved into two **1:M relationships** using a third table called a **Junction Table** (like our `user_badges` example) which uses a **Composite Key** to link the two parent tables.

### 3.7 Normalization
Normalization is the process of optimizing a database structure to reduce **Data Redundancy** (repeated information) and eliminate **Update Anomalies**.

#### The Three Normal Forms (NF)
| Form | Requirement | Goal |
|------|-------------|------|
| **1NF** (First Normal Form) | Attributes must be **atomic** (no multi-valued fields). No repeating groups. | Ensure basic table structure. |
| **2NF** (Second Normal Form) | Must be in 1NF AND all non-key attributes must be **fully functionally dependent** on the *entire* primary key. | Eliminate **Partial Dependencies**. |
| **3NF** (Third Normal Form) | Must be in 2NF AND no non-key attribute can depend on another non-key attribute. | Eliminate **Transitive Dependencies**. |

**Aha! Moment**: Normalization ensures that every piece of data is stored in exactly one place, making the database easier to maintain and faster to update safely.


---

## 4. Modifying Databases: Read vs Write Operations
> 📚 **Purpose**: Differentiate between querying data and altering database records.
> 🎯 **Goal**: Understand the risks and requirements of data manipulation versus analysis.

As we've mentioned throughout this course, there are many times we might find ourselves using SQL or a SQL-like query language on a database. We can think of some uses as "read-only operations" and other uses as "read/write operations".

### 4.1 Read-Only Operations (Data Analysis)
An example of a "read-only operation" is a data analysis on a data dump from some app or research study. 

**Scenario**: A data scientist working for a daily diary wants to understand if exercise makes people want to reward themselves with sweets.
```sql
-- Query: What percentage of users eat ice cream on the same day they run?
SELECT * FROM diary_logs 
WHERE food LIKE "%ice cream%" AND activity LIKE "%running%";
```
In data analysis, pretty much everything is a `SELECT`—it's all read-only. We are querying existing data without creating new records. In this path, you need to master `SELECT` queries, but you may not need to know how to create tables or update rows.

### 4.2 Read/Write Operations (Software Engineering)
An example of "read/write operations" is a software engineer creating the backend for a webapp.

**Scenario**: A software engineer working on a health tracker writes code to insert a new daily log whenever a user submits a form.
```sql
INSERT INTO diary_logs (id, food, activity)
VALUES (123, "ice cream", "running");
```

**Integration with Programming Languages**:
These commands are often issued from inside a server-side language using a library like **SQLAlchemy** for Python:
```python
# Example SQLAlchemy Insertion
diary_logs.insert().values(id=123, food="ice cream", activity='running')
```

### 4.3 The Risks of Write Operations
Beyond insertions, software engineers must write SQL to modify the database when users edit logs, delete entries, or close accounts. If features are added (like an "emotion" column to track happiness while eating ice cream), the **table schema** itself must be modified.

- **Safe**: `INSERT` (adds data).
- **Dangerous**: `UPDATE`, `DELETE`, `DROP`, or `ALTER` (modifies or removes existing data).

Understanding these operations deeply is essential for maintaining data integrity. Keep going to learn how to use them!

---

## 5. 🗣️ SQL Basics: CREATE & INSERT
> 📚 **Purpose**: Learn the fundamental commands for building tables and adding data.
> 🎯 **Goal**: Successfully define database schemas and populate them with initial records.

### Scenario 1: Basic Grocery List

**Scenario**: Building a grocery list database

```sql
CREATE TABLE groceries (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER);
```

**Column Definitions**:
- `id`: Unique identifier for each row (`INTEGER PRIMARY KEY`)
- `name`: Item name (`TEXT`)
- `quantity`: How many to buy (`INTEGER`)

### Inserting Data

**Adding items to the table**:

```sql
INSERT INTO groceries VALUES (1, "Bananas", 4);
INSERT INTO groceries VALUES (2, "Peanut Butter", 1);
INSERT INTO groceries VALUES (3, "Dark chocolate bars", 2);
```

### Expanded Table with Aisle Information

**Adding an aisle column**:

```sql
CREATE TABLE groceries (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER, aisle INTEGER);
```

**Adding grocery items with aisle numbers**:

```sql
/** Grocery list: 
Bananas (4) | Aisle 7
Peanut Butter (1) | Aisle 2
Dark Chocolate Bars (2) | Aisle 2
Ice cream (1) | Aisle 12
Cherries (6) | Aisle 2
Chocolate syrup (1) | Aisle 4
**/

INSERT INTO groceries VALUES (1, "Bananas", 4, 7);
INSERT INTO groceries VALUES(2, "Peanut Butter", 1, 2);
INSERT INTO groceries VALUES(3, "Dark Chocolate Bars", 2, 2);
INSERT INTO groceries VALUES(4, "Ice cream", 1, 12);
INSERT INTO groceries VALUES(5, "Cherries", 6, 2);
INSERT INTO groceries VALUES(6, "Chocolate syrup", 1, 4);

### Case Study: Exercise Tracker (AUTOINCREMENT & Specifying Columns)

**Scenario**: Tracking daily exercise activities.

```sql
CREATE TABLE exercise_logs
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    minutes INTEGER, 
    calories INTEGER,
    heart_rate INTEGER);
```

**Key Concepts**:
- **`AUTOINCREMENT`**: The database automatically assigns the next available ID (usually one higher than the current max).
- **Specifying Columns**: By listing column names after the table name, you only need to provide values for those specific columns. This is the preferred way to `INSERT` data when using auto-incrementing IDs.

**Inserting Data**:

```sql
INSERT INTO exercise_logs(type, minutes, calories, heart_rate) VALUES ("biking", 30, 100, 110);
INSERT INTO exercise_logs(type, minutes, calories, heart_rate) VALUES ("biking", 10, 30, 105);
INSERT INTO exercise_logs(type, minutes, calories, heart_rate) VALUES ("dancing", 15, 200, 120);
```

---

## 6. SQL Queries: SELECT, ORDER BY, WHERE
> 📚 **Purpose**: Master the core tools for retrieving and filtering data from tables.
> 🎯 **Goal**: Write precise queries to extract specific information and organize results.

### Basic SELECT Query

**Retrieve all rows**:
```sql
SELECT * FROM groceries;
```

- `SELECT *`: Select all columns
- `FROM groceries`: From the groceries table
- Results displayed in the order columns were created

### SELECT with Specific Columns

**Get only the name column**:
```sql
SELECT name FROM groceries;
```

**Get specific columns only** (more efficient than `*`):
```sql
SELECT name, quantity FROM groceries;
```

### ORDER BY Clause

**Sort results by aisle**:
```sql
SELECT * FROM groceries ORDER BY aisle;
```

**Why it matters**:
- Organizes items logically (e.g., by store aisle)
- Makes shopping more efficient
- Results ordered top-to-bottom by aisle number

### WHERE Clause - Filtering Data

**Filter results with conditions**:
```sql
SELECT * FROM groceries WHERE aisle > 5;
```

**Comparison Operators**:
- `>` (greater than)
- `<` (less than)
- `=` (equal to)
- `>=` (greater than or equal)
- `<=` (less than or equal)
- `<>` or `!=` (not equal)
- `LIKE` (pattern matching)
- `IN` (multiple values)

### Multiple Conditions: AND & OR

To filter data more precisely, you can combine conditions using logical operators.

**The `AND` Operator**:
Returns rows only if **all** conditions are true.

```sql
-- Find activities that burned > 50 calories AND took < 30 minutes
SELECT * FROM exercise_logs WHERE calories > 50 AND minutes < 30;
```

**The `OR` Operator**:
Returns rows if **at least one** condition is true.

```sql
-- Find vigorous exercises: calories > 50 OR heart_rate > 100
SELECT * FROM exercise_logs WHERE calories > 50 OR heart_rate > 100;
```

**Operator Precedence**:
- **`AND` takes precedence over `OR`**. This means `AND` conditions are evaluated first.
- **Parentheses `()`** can be used to override this precedence or to make the query more readable, similar to mathematical expressions.

### Case Study: Songs Library (More complex queries with AND/OR)

**Scenario**: Managing a library of songs with various moods and release dates.

```sql
CREATE TABLE songs (
    id INTEGER PRIMARY KEY,
    title TEXT,
    artist TEXT,
    mood TEXT,
    duration INTEGER,
    released INTEGER);
    
INSERT INTO songs (title, artist, mood, duration, released)
    VALUES ("Bohemian Rhapsody", "Queen", "epic", 60, 1975);
INSERT INTO songs (title, artist, mood, duration, released)
    VALUES ("Let it go", "Idina Menzel", "epic", 227, 2013);
INSERT INTO songs (title, artist, mood, duration, released)
    VALUES ("I will survive", "Gloria Gaynor", "epic", 198, 1978);
INSERT INTO songs (title, artist, mood, duration, released)
    VALUES ("Twist and Shout", "The Beatles", "happy", 152, 1963);
INSERT INTO songs (title, artist, mood, duration, released)
    VALUES ("La Bamba", "Ritchie Valens", "happy", 166, 1958);
INSERT INTO songs (title, artist, mood, duration, released)
    VALUES ("I will always love you", "Whitney Houston", "epic", 273, 1992);
INSERT INTO songs (title, artist, mood, duration, released)
    VALUES ("Sweet Caroline", "Neil Diamond", "happy", 201, 1969);
INSERT INTO songs (title, artist, mood, duration, released)
    VALUES ("Call me maybe", "Carly Rae Jepsen", "happy", 193, 2011);
```

**Query Examples**:

```sql
-- Retrieve all song titles
SELECT title FROM songs;

-- Find songs that are 'epic' OR released after 1990
SELECT title FROM songs WHERE mood IS 'epic' OR released > 1990;

-- Find 'epic' songs released after 1990 that are shorter than 4 minutes (240 seconds)
SELECT title FROM songs WHERE mood IS 'epic' AND released > 1990 AND duration < 240;
```

### Combining ORDER BY with WHERE

**Complete query example**:
```sql
SELECT * FROM groceries 
WHERE aisle > 5 
ORDER BY aisle;
```

**Use case**: 
- Filter items in aisles 6-12
- Order results to shop efficiently
- Split shopping between two people

---

## 7. Advanced Filtering: IN, Subqueries, & LIKE
> 📚 **Purpose**: Utilize complex filtering techniques for sophisticated data retrieval.
> 🎯 **Goal**: Implement pattern matching and nested queries to handle elaborate search criteria.

### The IN Operator

The `IN` operator allows you to specify multiple values in a `WHERE` clause. It is a shorthand for multiple `OR` conditions, making your queries cleaner and easier to read.

**Example: Selecting Outdoor Activities**

Instead of writing:
```sql
SELECT * FROM exercise_logs 
WHERE type = "biking" OR type = "hiking" OR type = "tree climbing" OR type = "rowing";
```

You can write:
```sql
SELECT * FROM exercise_logs 
WHERE type IN ("biking", "hiking", "tree climbing", "rowing");
```

**Inverse Filtering with `NOT IN`**:
```sql
-- Find only indoor activities
SELECT * FROM exercise_logs 
WHERE type NOT IN ("biking", "hiking", "tree climbing", "rowing");
```

### Subqueries

A **subquery** is a query nested inside another query. This allows you to perform complex filtering that stays up-to-date as your data changes.

**Scenario**: You have a table of doctor-recommended activities (`drs_favorites`).

```sql
CREATE TABLE drs_favorites
    (id INTEGER PRIMARY KEY,
    type TEXT,
    reason TEXT);

INSERT INTO drs_favorites(type, reason) VALUES ("biking", "Improves endurance and flexibility.");
INSERT INTO drs_favorites(type, reason) VALUES ("hiking", "Increases cardiovascular health.");
```

**Using a Subquery to Filter Logs**:
```sql
-- Select all logs that match a doctor's favorite activity
SELECT * FROM exercise_logs WHERE type IN (
    SELECT type FROM drs_favorites);
```

### The LIKE Operator & Wildcards

The `LIKE` operator is used for **inexact matches** (pattern matching). It is often combined with subqueries to find data based on keywords.

**Wildcards**:
- `%`: Represents zero, one, or multiple characters.

**Example: Filtering by Keyword**:
```sql
-- Find exercises recommended for "cardiovascular" reasons
SELECT * FROM exercise_logs WHERE type IN (
    SELECT type FROM drs_favorites WHERE reason LIKE "%cardiovascular%");
```

### Case Study: Artist & Song Subqueries

**Scenario**: Filtering songs based on artist metadata (like genre) using nested queries.

```sql
CREATE TABLE artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    country TEXT,
    genre TEXT);

INSERT INTO artists (name, country, genre) VALUES ("Taylor Swift", "US", "Pop");
INSERT INTO artists (name, country, genre) VALUES ("Led Zeppelin", "US", "Hard rock");
INSERT INTO artists (name, country, genre) VALUES ("ABBA", "Sweden", "Disco");
INSERT INTO artists (name, country, genre) VALUES ("Queen", "UK", "Rock");
INSERT INTO artists (name, country, genre) VALUES ("Celine Dion", "Canada", "Pop");
INSERT INTO artists (name, country, genre) VALUES ("Meatloaf", "US", "Hard rock");
INSERT INTO artists (name, country, genre) VALUES ("Garth Brooks", "US", "Country");
INSERT INTO artists (name, country, genre) VALUES ("Shania Twain", "Canada", "Country");
INSERT INTO artists (name, country, genre) VALUES ("Rihanna", "US", "Pop");
INSERT INTO artists (name, country, genre) VALUES ("Guns N' Roses", "US", "Hard rock");
INSERT INTO artists (name, country, genre) VALUES ("Gloria Estefan", "US", "Pop");
INSERT INTO artists (name, country, genre) VALUES ("Bob Marley", "Jamaica", "Reggae");

CREATE TABLE songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist TEXT,
    title TEXT);

INSERT INTO songs (artist, title) VALUES ("Taylor Swift", "Shake it off");
INSERT INTO songs (artist, title) VALUES ("Rihanna", "Stay");
INSERT INTO songs (artist, title) VALUES ("Celine Dion", "My heart will go on");
INSERT INTO songs (artist, title) VALUES ("Celine Dion", "A new day has come");
INSERT INTO songs (artist, title) VALUES ("Shania Twain", "Party for two");
INSERT INTO songs (artist, title) VALUES ("Gloria Estefan", "Conga");
INSERT INTO songs (artist, title) VALUES ("Led Zeppelin", "Stairway to heaven");
INSERT INTO songs (artist, title) VALUES ("ABBA", "Mamma mia");
INSERT INTO songs (artist, title) VALUES ("Queen", "Bicycle Race");
INSERT INTO songs (artist, title) VALUES ("Queen", "Bohemian Rhapsody");
INSERT INTO songs (artist, title) VALUES ("Guns N' Roses", "Don't cry");
```

**Querying Across Tables**:

```sql
-- 1. Find all songs by Queen
SELECT title FROM songs WHERE artist = 'Queen';

-- 2. Find all artists in the 'Pop' genre
SELECT name FROM artists WHERE genre = 'Pop';

-- 3. Complex Query: Find all song titles for all Pop artists
SELECT title FROM songs WHERE artist IN (
    SELECT name FROM artists WHERE genre = 'Pop');
```

---

## 8. Aggregating Data: GROUP BY & HAVING
> 📚 **Purpose**: Summarize large datasets by grouping related information and calculating metrics.
> 🎯 **Goal**: Perform statistical analysis across data categories to derive high-level insights.

Aggregation allows you to summarize data by grouping rows and performing calculations across those groups.

### GROUP BY and Aggregate Functions

The `GROUP BY` clause is used to group rows that have the same values in specified columns. You can then use **aggregate functions** like `SUM()`, `AVG()`, `COUNT()`, `MIN()`, or `MAX()` to calculate values for each group.

**Example: Total Calories per Activity Type**
```sql
SELECT type, SUM(calories) FROM exercise_logs GROUP BY type;
```

### Column Aliasing with `AS`

You can rename result columns using the `AS` keyword to make them more readable and easier to reference.

```sql
SELECT type, SUM(calories) AS total_calories 
FROM exercise_logs 
GROUP BY type;
```

### Filtering Grouped Results with `HAVING`

While `WHERE` filters individual rows **before** they are grouped, `HAVING` filters the results **after** they have been grouped and aggregated.

**Example: Filter by Total Calories**
To find activity types where the *total* calories burned is greater than 150:

```sql
SELECT type, SUM(calories) AS total_calories 
FROM exercise_logs
GROUP BY type
HAVING total_calories > 150;
```

**Common Aggregate Functions with `HAVING`**:

- **Average**: Filter activities with an average calorie burn > 70.
  ```sql
  SELECT type, AVG(calories) AS avg_calories 
  FROM exercise_logs
  GROUP BY type
  HAVING avg_calories > 70;
  ```

- **Count**: Find activities logged at least twice.
  ```sql
  SELECT type 
  FROM exercise_logs 
  GROUP BY type 
  HAVING COUNT(*) >= 2;
  ```

### Case Study: Book Authors & Word Counts

**Scenario**: Analyzing the total and average word counts for authors with multiple books.

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT,
    title TEXT,
    words INTEGER);
    
INSERT INTO books (author, title, words) VALUES ("J.K. Rowling", "Harry Potter and the Philosopher's Stone", 79944);
INSERT INTO books (author, title, words) VALUES ("J.K. Rowling", "Harry Potter and the Chamber of Secrets", 85141);
INSERT INTO books (author, title, words) VALUES ("J.K. Rowling", "Harry Potter and the Prisoner of Azkaban", 107253);
INSERT INTO books (author, title, words) VALUES ("J.K. Rowling", "Harry Potter and the Goblet of Fire", 190637);
INSERT INTO books (author, title, words) VALUES ("J.K. Rowling", "Harry Potter and the Order of the Phoenix", 257045);
INSERT INTO books (author, title, words) VALUES ("J.K. Rowling", "Harry Potter and the Half-Blood Prince", 168923);
INSERT INTO books (author, title, words) VALUES ("J.K. Rowling", "Harry Potter and the Deathly Hallows", 197651);
INSERT INTO books (author, title, words) VALUES ("Stephenie Meyer", "Twilight", 118501);
INSERT INTO books (author, title, words) VALUES ("Stephenie Meyer", "New Moon", 132807);
INSERT INTO books (author, title, words) VALUES ("Stephenie Meyer", "Eclipse", 147930);
INSERT INTO books (author, title, words) VALUES ("Stephenie Meyer", "Breaking Dawn", 192196);
INSERT INTO books (author, title, words) VALUES ("J.R.R. Tolkien", "The Hobbit", 95022);
INSERT INTO books (author, title, words) VALUES ("J.R.R. Tolkien", "Fellowship of the Ring", 177227);
INSERT INTO books (author, title, words) VALUES ("J.R.R. Tolkien", "Two Towers", 143436);
INSERT INTO books (author, title, words) VALUES ("J.R.R. Tolkien", "Return of the King", 134462);
```

**Analyzing Grouped Data**:

```sql
-- Find authors who have written more than 1,000,000 words total
SELECT author, SUM(words) AS total_words 
FROM books 
GROUP BY author 
HAVING total_words > 1000000;

-- Find authors whose books average more than 150,000 words
SELECT author, AVG(words) AS avg_words 
FROM books 
GROUP BY author 
HAVING avg_words > 150000;
```

---

## 9. Conditional Logic: The CASE Statement
> 📚 **Purpose**: Apply conditional logic directly within SQL queries to categorize or transform data.
> 🎯 **Goal**: Create virtual columns and labels based on specific data values.

SQL allows you to perform calculations and apply conditional logic within your queries using math operators and the `CASE` statement.

### Mathematical Operators

You can use standard math operators in your `SELECT` and `WHERE` clauses:
- `+` (addition), `-` (subtraction), `*` (multiplication), `/` (division).
- **Parentheses `()`** are used to control the order of evaluation.

**Example: Basic Calculation**
```sql
-- Find exercises where heart rate is above max (220 - age)
SELECT COUNT(*) FROM exercise_logs WHERE heart_rate > 220 - 30;
```

### The ROUND() Function

The `ROUND()` function is used to round a numeric value to a specified number of decimal places.

```sql
-- Check if heart rate is within 50-90% of max
SELECT COUNT(*) FROM exercise_logs 
WHERE heart_rate >= ROUND(0.50 * (220-30)) 
AND heart_rate <= ROUND(0.90 * (220-30));
```

### The CASE Statement

The `CASE` statement is like an `if/then/else` block. It allows you to create new, "virtual" columns based on conditions in your data.

**Syntax**:
```sql
CASE 
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ELSE result_else
END as "column_name"
```

### Case Study: Heart Rate Zones

**Categorizing Heart Rate Logs**:
```sql
SELECT type, heart_rate,
    CASE 
        WHEN heart_rate > 220-30 THEN "above max"
        WHEN heart_rate > ROUND(0.90 * (220-30)) THEN "above target"
        WHEN heart_rate > ROUND(0.50 * (220-30)) THEN "within target"
        ELSE "below target"
    END as "hr_zone"
FROM exercise_logs;
```

**Summarizing with CASE**:
Once you've created a category with `CASE`, you can use it in a `GROUP BY` clause to summarize your data.

```sql
SELECT COUNT(*),
    CASE 
        WHEN heart_rate > 220-30 THEN "above max"
        WHEN heart_rate > ROUND(0.90 * (220-30)) THEN "above target"
        WHEN heart_rate > ROUND(0.50 * (220-30)) THEN "within target"
        ELSE "below target"
    END as "hr_zone"
FROM exercise_logs
GROUP BY hr_zone;
```

### Case Study: Student Grades

**Scenario**: Converting numeric grades and completion fractions into percentages and letter grades.

```sql
CREATE TABLE student_grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    number_grade INTEGER,
    fraction_completed REAL);
    
INSERT INTO student_grades (name, number_grade, fraction_completed) VALUES ("Winston", 90, 0.805);
INSERT INTO student_grades (name, number_grade, fraction_completed) VALUES ("Winnefer", 95, 0.901);
INSERT INTO student_grades (name, number_grade, fraction_completed) VALUES ("Winsteen", 85, 0.906);
INSERT INTO student_grades (name, number_grade, fraction_completed) VALUES ("Wincifer", 66, 0.7054);
INSERT INTO student_grades (name, number_grade, fraction_completed) VALUES ("Winster", 76, 0.5013);
INSERT INTO student_grades (name, number_grade, fraction_completed) VALUES ("Winstonia", 82, 0.9045);
```

**Calculating Percentages & Letter Grades**:

```sql
-- 1. Calculate completion percentage using ROUND
SELECT name, number_grade, ROUND(100 * fraction_completed) AS percent_completed 
FROM student_grades;

-- 2. Categorize and summarize by Letter Grade
SELECT COUNT(*), 
    CASE
        WHEN number_grade > 90 THEN "A"
        WHEN number_grade > 80 THEN "B"
        WHEN number_grade > 70 THEN "C"
        ELSE "F"
    END as "letter_grade"
FROM student_grades
GROUP BY letter_grade;
```

---

## 10. JOINing Related Tables
> 📚 **Purpose**: Learn how to combine data from multiple related tables to create comprehensive result sets.
> 🎯 **Goal**: Master implicit and explicit JOIN syntax to link datasets and perform multi-table analysis.

In most professional databases, data is split across multiple tables to reduce redundancy (Normalization). To get a complete picture, you must "join" these tables back together.

### 10.1 Scenario: Students and Grades
Imagine a database with two related tables:
1.  **`students`**: Detailed info (name, email) with an `id`.
2.  **`student_grades`**: Test results linked to students via `student_id`.

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT);

INSERT INTO students (first_name, last_name, email)
    VALUES ("Peter", "Rabbit", "peter@rabbit.com");
INSERT INTO students (first_name, last_name, email)
    VALUES ("Alice", "Wonderland", "alice@wonderland.com");
    
CREATE TABLE student_grades (id INTEGER PRIMARY KEY,
    student_id INTEGER,
    test TEXT,
    grade INTEGER);

INSERT INTO student_grades (student_id, test, grade)
    VALUES (1, "Nutrition", 95);
INSERT INTO student_grades (student_id, test, grade)
    VALUES (2, "Nutrition", 92);
```

### 10.2 The Cross Join
The simplest join is a **Cross Join**, which pairs every row of the first table with every row of the second.

```sql
/* Cross Join Syntax */
SELECT * FROM student_grades, students;
```
**Result**: If you have 2 students and 4 grades, you get 8 rows. While simple, it's rarely useful because it matches unrelated data.

### 10.3 Implicit Inner Join
To only see grades next to the correct student, we can use an **Implicit Inner Join** by adding a `WHERE` clause.

```sql
/* Implicit Inner Join */
SELECT * FROM student_grades, students
    WHERE student_grades.student_id = students.id;
```
This filters the cross join to only show rows where the IDs match.

### 10.4 Explicit Inner Join (Best Practice)
The professional way to link tables is the **Explicit Inner Join** using the `JOIN` and `ON` keywords.

```sql
/* Explicit Inner Join */
SELECT students.first_name, students.last_name, students.email, student_grades.test, student_grades.grade 
FROM students
JOIN student_grades
ON students.id = student_grades.student_id;
```

### 10.5 Filtering Joined Results
Once tables are joined, you can still use `WHERE`, `ORDER BY`, and `GROUP BY`.

```sql
/* Finding high-achievers */
SELECT students.first_name, student_grades.grade 
FROM students
JOIN student_grades ON students.id = student_grades.student_id
WHERE student_grades.grade > 90;
```

### 10.6 Pro-Tip: Column Prefixing
If multiple tables have columns with the same name (like a `grade` column in `students` for their overall GPA), SQL won't know which one to pick. **Always prefix your columns** with the table name for clarity and safety.

`students.first_name` vs `student_grades.grade`

### 10.7 Case Study: Persons & Hobbies
This example demonstrates a many-to-one relationship where multiple hobbies can be linked to a single person.

```sql
/* 1. Setup Tables */
CREATE TABLE persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER);
    
INSERT INTO persons (name, age) VALUES ("Bobby McBobbyFace", 12);
INSERT INTO persons (name, age) VALUES ("Lucy BoBucie", 25);
INSERT INTO persons (name, age) VALUES ("Banana FoFanna", 14);
INSERT INTO persons (name, age) VALUES ("Shish Kabob", 20);
INSERT INTO persons (name, age) VALUES ("Fluffy Sparkles", 8);
INSERT INTO persons (name,age) VALUES ("Funky Toes",51);

CREATE table hobbies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    name TEXT);
    
INSERT INTO hobbies (person_id, name) VALUES (1, "drawing");
INSERT INTO hobbies (person_id, name) VALUES (1, "coding");
INSERT INTO hobbies (person_id, name) VALUES (2, "dancing");
INSERT INTO hobbies (person_id, name) VALUES (2, "coding");
INSERT INTO hobbies (person_id, name) VALUES (3, "skating");
INSERT INTO hobbies (person_id, name) VALUES (3, "rowing");
INSERT INTO hobbies (person_id, name) VALUES (3, "drawing");
INSERT INTO hobbies (person_id, name) VALUES (4, "coding");
INSERT INTO hobbies (person_id, name) VALUES (4, "dilly-dallying");
INSERT INTO hobbies (person_id, name) VALUES (4, "meowing");
INSERT INTO hobbies (person_id, name) VALUES (5, "yodeling");

/* 2. Execute JOIN to associate Names with Hobbies */
SELECT persons.name, hobbies.name
FROM persons, hobbies
WHERE persons.id = hobbies.person_id;
```

---

## 11. OUTER JOINs
> 📚 **Purpose**: Understand how to retain records that don't have matching keys in joined tables.
> 🎯 **Goal**: Master `LEFT OUTER JOIN` to create comprehensive reports that include "missing" or unlinked data.

While `INNER JOIN` is useful for finding matching records, it often hides data that doesn't have a direct link. `OUTER JOIN`s solve this by ensuring certain rows are kept even if there is no match in the other table.

### 11.1 The "Missing Alice" Problem
Imagine we have our `students` table and a new `student_projects` table.

```sql
CREATE TABLE student_projects (id INTEGER PRIMARY KEY,
    student_id INTEGER,
    title TEXT);
    
INSERT INTO student_projects (student_id, title)
    VALUES (1, "Carrotapault");
```

If we run an `INNER JOIN` to see names and projects:
```sql
SELECT students.first_name, student_projects.title
FROM students
JOIN student_projects
ON students.id = student_projects.student_id;
```
**Result**: We only see "Peter" and his "Carrotapault". **Alice disappears** because she doesn't have a project yet.

### 11.2 Using LEFT OUTER JOIN
A `LEFT OUTER JOIN` tells SQL to keep every row from the "left" table (the one after the `FROM` keyword) even if there is no matching record in the "right" table.

```sql
/* Retain every student, even those without projects */
SELECT students.first_name, students.last_name, student_projects.title
FROM students
LEFT OUTER JOIN student_projects
ON students.id = student_projects.student_id;
```
**Result**: Alice now appears in the list, with a `NULL` value for the project title. This is much better for comprehensive reporting.

### 11.3 Other Outer Join Types
- **RIGHT OUTER JOIN**: Keeps everything from the "right" table. (In many environments like SQLite, you can achieve this by just swapping the table order in a `LEFT JOIN`).
- **FULL OUTER JOIN**: Keeps rows from both tables, filling in `NULL`s on either side where no match exists.

> 💡 **Adaptability**: Not every SQL environment supports every type of join (e.g., SQLite doesn't support `RIGHT` or `FULL` natively). Learning to adapt your tools to your specific database environment is a key skill for any developer.

### 11.4 Case Study: Customer Orders (Aggregation with OUTER JOIN)
This challenge demonstrates how to combine `LEFT JOIN` with aggregate functions like `SUM()` and `GROUP BY` to generate a financial summary for all customers, even those without orders.

```sql
/* 1. Setup Tables */
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT);
    
INSERT INTO customers (name, email) VALUES ("Doctor Who", "doctorwho@timelords.com");
INSERT INTO customers (name, email) VALUES ("Harry Potter", "harry@potter.com");
INSERT INTO customers (name, email) VALUES ("Captain Awesome", "captain@awesome.com");

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    item TEXT,
    price REAL);

INSERT INTO orders (customer_id, item, price)
    VALUES (1, "Sonic Screwdriver", 1000.00);
INSERT INTO orders (customer_id, item, price)
    VALUES (2, "High Quality Broomstick", 40.00);
INSERT INTO orders (customer_id, item, price)
    VALUES (1, "TARDIS", 1000000.00);

/* 2. Detailed Join (See every order) */
SELECT customers.name, customers.email, orders.item, orders.price
FROM customers
LEFT JOIN orders
ON customers.id = orders.customer_id;

/* 3. Aggregated Join (One row per customer with total spent) */
-- Goal: Sort by total money spent, most to least.
SELECT 
   customers.name,
   customers.email,
   SUM(orders.price) AS total_spent
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
GROUP BY customers.id
ORDER BY total_spent DESC;
```

---

## 12. Self Joins
> 📚 **Purpose**: Explain how to relate records within the same table by joining it with itself.
> 🎯 **Goal**: Master the use of table aliases to resolve column ambiguity in self-referential relationships.

A **Self Join** occurs when you join a table to itself. This is useful when a column in a table refers to another column in the same table (e.g., an `employee_id` referring to a `manager_id`).

### 12.1 Scenario: Student Buddies
Imagine our `students` table has a `buddy_id` column that refers to the `id` of another student in the same table.

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    buddy_id INTEGER);

INSERT INTO students VALUES (1, "Peter", "Rabbit", "peter@rabbit.com", 2);
INSERT INTO students VALUES (2, "Alice", "Wonderland", "alice@wonderland.com", 1);
INSERT INTO students VALUES (3, "Aladdin", "Lampland", "aladdin@lampland.com", 4);
INSERT INTO students VALUES (4, "Simba", "Kingston", "simba@kingston.com", 3);
```

### 12.2 The Challenge: Column Ambiguity
If we try to join `students` with `students`, SQL will return an error stating that column names like `first_name` are **ambiguous** because they exist in both "versions" of the table.

### 12.3 Solution: Table Aliases
To distinguish between the two instances of the same table, we give them **Aliases** (nicknames).

```sql
/* Self Join: Link students to their buddies */
SELECT 
    students.first_name, 
    students.last_name, 
    buddies.email AS buddy_email
FROM students
JOIN students buddies
ON students.buddy_id = buddies.id;
```

**How it works**:
1.  We refer to the first instance simply as `students`.
2.  We refer to the second instance as `buddies` using the syntax `JOIN students buddies`.
3.  The `ON` clause links the `buddy_id` from the primary side to the `id` of the aliased side.

### 12.4 Case Study: Harry Potter Movies (Self OUTER JOIN)
This advanced example demonstrates combining a **Self Join** with an **Outer Join**. We want to list every movie next to its sequel, even if it's the final movie in the series (which has no sequel).

```sql
/* 1. Setup Table */
CREATE TABLE movies (id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    released INTEGER,
    sequel_id INTEGER);

INSERT INTO movies VALUES (1, "HP and the Philosopher's Stone", 2001, 2);
INSERT INTO movies VALUES (2, "HP and the Chamber of Secrets", 2002, 3);
INSERT INTO movies VALUES (3, "HP and the Prisoner of Azkaban", 2004, 4);
INSERT INTO movies VALUES (4, "HP and the Goblet of Fire", 2005, 5);
INSERT INTO movies VALUES (5, "HP and the Order of the Phoenix", 2007, 6);
INSERT INTO movies VALUES (6, "HP and the Half-Blood Prince", 2009, 7);
INSERT INTO movies VALUES (7, "HP and the Deathly Hallows – Part 1", 2010, 8);
INSERT INTO movies VALUES (8, "HP and the Deathly Hallows – Part 2", 2011, NULL);

/* 2. Execute Self OUTER JOIN */
-- We use LEFT OUTER JOIN to ensure the final movie (ID 8) is still listed
SELECT 
    movies.title, 
    sequel.title AS sequel_title
FROM movies
LEFT OUTER JOIN movies sequel
  ON movies.sequel_id = sequel.id;
```

---

## 13. Combining Multiple Joins
> 📚 **Purpose**: Learn how to connect three or more tables (or the same table multiple times) in a single query.
> 🎯 **Goal**: Balance query complexity with performance while generating multi-dimensional reports.

In complex databases, the information you need might be scattered across several tables. You can chain as many `JOIN` statements as necessary to bring that data together.

### 13.1 Scenario: Peer Reviews
Imagine we want students to review each other's projects. We have a `project_pairs` table that simply stores two project IDs.

```sql
CREATE TABLE project_pairs (id INTEGER PRIMARY KEY,
    project1_id INTEGER,
    project2_id INTEGER);

INSERT INTO project_pairs (project1_id, project2_id) VALUES(1, 2);
INSERT INTO project_pairs (project1_id, project2_id) VALUES(3, 4);
```

### 13.2 Chaining JOINs with Aliases
To show the actual **titles** of both projects in the pair, we must join `project_pairs` with `student_projects` **twice**.

```sql
/* Combine Joins and Self Joins */
SELECT 
    a.title AS project1_title, 
    b.title AS project2_title 
FROM project_pairs
JOIN student_projects a ON project_pairs.project1_id = a.id
JOIN student_projects b ON project_pairs.project2_id = b.id;
```

**Key Mechanics**:
1.  **Multiple JOIN Keywords**: Use `JOIN` again for every new connection.
2.  **Unique Aliases**: We used `a` and `b` to distinguish between the two instances of `student_projects`.
3.  **Specific ON Clauses**: Each join needs its own logic to link the correct IDs.

### 13.3 Performance Considerations
While SQL allows for many joins, keep in mind:
- **Speed**: Every join increases the computational work. More joins generally mean slower queries.
- **Complexity**: Highly joined queries can become difficult to debug.
- **Optimization**: We will cover how to analyze and improve query efficiency in future chapters.

### 13.4 Case Study: FriendBook
This challenge demonstrates joining personal profile data with activity logs in a social networking context.

```sql
/* 1. Setup Tables */
CREATE TABLE persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    age INTEGER);
    
INSERT INTO persons (fullname, age) VALUES ("Bobby McBobbyFace", "12");
INSERT INTO persons (fullname, age) VALUES ("Lucy BoBucie", "25");
INSERT INTO persons (fullname, age) VALUES ("Banana FoFanna", "14");
INSERT INTO persons (fullname, age) VALUES ("Shish Kabob", "20");
INSERT INTO persons (fullname, age) VALUES ("Fluffy Sparkles", "8");

CREATE table hobbies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    name TEXT);
    
INSERT INTO hobbies (person_id, name) VALUES (1, "drawing");
INSERT INTO hobbies (person_id, name) VALUES (1, "coding");
INSERT INTO hobbies (person_id, name) VALUES (2, "dancing");
INSERT INTO hobbies (person_id, name) VALUES (2, "coding");
INSERT INTO hobbies (person_id, name) VALUES (3, "skating");
INSERT INTO hobbies (person_id, name) VALUES (3, "rowing");
INSERT INTO hobbies (person_id, name) VALUES (3, "drawing");
INSERT INTO hobbies (person_id, name) VALUES (4, "coding");
INSERT INTO hobbies (person_id, name) VALUES (4, "dilly-dallying");
INSERT INTO hobbies (person_id, name) VALUES (4, "meowing");

CREATE table friends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person1_id INTEGER,
    person2_id INTEGER);

INSERT INTO friends (person1_id, person2_id) VALUES (1, 4);
INSERT INTO friends (person1_id, person2_id) VALUES (2, 3);

/* Step 1: Execute JOIN to show Names with Hobbies */
SELECT persons.fullname AS names, hobbies.name AS hobby_name
FROM persons
JOIN hobbies ON persons.id = hobbies.person_id;

/* Step 2: Advanced Multi-Join to resolve Friend Pairs */
-- We join 'friends' with 'persons' TWICE using aliases 'a' and 'b'
SELECT 
    a.fullname AS person1, 
    b.fullname AS person2 
FROM friends
JOIN persons a ON friends.person1_id = a.id
JOIN persons b ON friends.person2_id = b.id;
```

---

## 14. Roles in the Ecosystem
> 📚 **Purpose**: Identify the various professional roles that interact with database systems.
> 🎯 **Goal**: Understand how data modelers, DBAs, and engineers collaborate within a data environment.

In a real-world company (like an exercise app with thousands of users), different team members use SQL for various purposes.

### Who Issues SQL Queries?

| Role | Responsibility | SQL Use Case |
|------|----------------|--------------|
| **Data Modeler** | Designs data structure and relationships | Defines how tables connect and how data is organized. |
| **Database Administrator (DBA)** | Maintains database, ensures security | Manages performance, backups, and access control. |
| **Software Engineer / Backend Developer** | Builds the app's backend and frontend. | Uses SQL on the server-side to fetch data for user dashboards and to handle data persistence (`INSERT`, `UPDATE`, `DELETE`). |
| **Data Scientist / Data Analyst** | Analyzes data to find patterns and trends. | Uses complex `SELECT` statements with `GROUP BY`, `CASE`, and `JOIN` to perform deep analysis and generate insights. |
| **Product Manager** | Makes decisions on how to improve the product. | Uses SQL to look at usage statistics (e.g., feature adoption) to make data-driven product decisions. |

### Role-Specific Scenarios

- **Software Engineer**: Fetches daily exercise logs for a user's personal dashboard using a `SELECT` filtered by user ID and date.
- **Data Scientist**: Analyzes whether morning exercisers are more likely to meet their weekly goals using `CASE` and `GROUP BY`.
- **Product Manager**: Audits the `heart_rate` field to see how many users are actually tracking it before deciding whether to deprecate the feature.

### Knowledge Sharing
Since these roles work together, they often share SQL knowledge. While not everyone needs to be an expert, a basic understanding of SQL helps everyone at a company make better, data-driven decisions.

---

## 15. Tools & Resources
> 📚 **Purpose**: Provide a curated list of software and learning materials for SQL mastery.
> 🎯 **Goal**: Equip learners with the necessary tools for practicing and extending their database knowledge.

| Tool | Use Case |
|------|----------|
| **SQLite** | Lightweight, browser-based practice |
| **PostgreSQL** | Advanced relational database |
| **MySQL** | Web applications |
| **MongoDB** | NoSQL, document storage |
| **DataGrip/SSMS** | Database management GUIs |

### Recommended Learning Resources
- **Khan Academy SQL Course**
- **SQLZoo**
- **Mode Analytics SQL Tutorial**
- **W3Schools SQL Tutorial**

---

## 🛠️ SQL Development Reference
> 📚 **Purpose**: Offer a concise cheat sheet for common SQL commands and syntax.
> 🎯 **Goal**: Serve as a quick-access guide during database development and querying tasks.

### Creating Tables
```sql
CREATE TABLE customers (
id INTEGER PRIMARY KEY, name TEXT, age INTEGER, weight REAL);
```

**Many Data Types**:
```sql
CREATE TABLE customers (
id INTEGER PRIMARY KEY, age INTEGER);
```

**Using Primary Keys**:
- Always specify a PRIMARY KEY for unique row identification
- See also: specifying defaults, using foreign keys
- For more details: [SQLite reference for CREATE](https://www.sqlite.org/lang_createtable.html)

### Inserting Data
```sql
-- Inserting data with all columns
INSERT INTO customers VALUES (73, "Brian", 33);

-- Inserting data specifying column names
INSERT INTO customers (name, age) VALUES ("Brian", 33);

-- See also: The SQLite reference for INSERT
```

### Querying Data
```sql
-- Select everything
SELECT * FROM customers;

-- Select unique values
SELECT DISTINCT country FROM artists;

-- Filter with conditions (AND, OR, NOT)
SELECT * FROM customers WHERE age > 21 AND NOT state = "NY";
SELECT * FROM exercise_logs WHERE calories > 50 OR heart_rate > 100;

-- Filter with ranges and sets (BETWEEN, IN)
SELECT * FROM songs WHERE released BETWEEN 1990 AND 2000;
SELECT * FROM customers WHERE plan IN ("free", "basic");

-- Filter with NULL values
SELECT * FROM exercise_logs WHERE heart_rate IS NULL;
SELECT * FROM exercise_logs WHERE heart_rate IS NOT NULL;

-- Pattern Matching with LIKE and Wildcards (%)
SELECT * FROM customers WHERE name LIKE "A%"; -- Starts with A
SELECT * FROM customers WHERE bio LIKE "%developer%"; -- Contains "developer"

-- Select specific columns with ALIASES
SELECT name AS customer_name, age FROM customers;

-- Order results and restrict output (LIMIT)
SELECT name, age FROM customers ORDER BY age DESC LIMIT 5;

-- Transform with CASE
SELECT name, CASE WHEN age > 18 THEN "adult" ELSE "minor" END AS type FROM customers;
```

### Aggregating Data
```sql
-- Aggregate functions (COUNT, AVG, SUM, MIN, MAX)
SELECT COUNT(*) FROM customers;
SELECT AVG(age), SUM(words), MIN(heart_rate), MAX(heart_rate) FROM exercise_logs;

-- Grouping data
SELECT gender, COUNT(*) FROM students GROUP BY gender;

-- Filtering grouped results with HAVING
SELECT type, SUM(calories) AS total FROM exercise_logs GROUP BY type HAVING total > 100;
```

### Joining Related Tables
See [Chapter 10: JOINing Related Tables](#10-joining-related-tables) for detailed examples of Cross, Implicit, and Explicit JOINs.

```sql
-- Explicit Inner Join (Best Practice)
SELECT students.first_name, student_grades.grade 
FROM students
JOIN student_grades ON students.id = student_grades.student_id;
```

### Joins and Set Operations
Merging data from multiple tables or combining result sets.

```sql
-- Inner Join: Returns rows with matching values in both tables
SELECT a.name, b.order_date FROM users a JOIN orders b ON a.id = b.user_id;

-- Left Join: Returns all rows from the left table, and matched rows from the right
SELECT a.name, b.order_date FROM users a LEFT JOIN orders b ON a.id = b.user_id;

-- Right Join: Returns all rows from the right table, and matched rows from the left
SELECT a.name, b.order_date FROM users a RIGHT JOIN orders b ON a.id = b.user_id;

-- Full Outer Join: Returns all rows when there is a match in either table
SELECT a.name, b.order_date FROM users a FULL OUTER JOIN orders b ON a.id = b.user_id;

-- Union: Combines result sets of two SELECT statements (Removes duplicates)
SELECT city FROM customers UNION SELECT city FROM suppliers;

-- Union All: Combines result sets of two SELECT statements (Keeps duplicates)
SELECT city FROM customers UNION ALL SELECT city FROM suppliers;
```

### Updating and Deleting Data
```sql
-- Updating data
UPDATE customers SET age = 33 WHERE id = 73;

-- Deleting data
DELETE FROM customers WHERE id = 73;
```

---

## 16. Changing rows with UPDATE and DELETE
> 📚 **Purpose**: Explain the mechanisms for modifying or removing existing data records.
> 🎯 **Goal**: Safely update information and manage deletions while maintaining data integrity.

Modifying existing data is a core part of application development. Whether a user is correcting a typo in a diary entry or deleting their account, you need commands that target specific rows safely.

### 16.1 Scenario: The Diary App
Imagine a basic setup with a `users` table and a `diary_logs` table.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT);
    
CREATE TABLE diary_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    date TEXT,
    content TEXT
    );
```

### 16.2 Updating Records (UPDATE)
When a user wants to modify a log they've already submitted, we use the `UPDATE` statement.

**Crucial Rule**: Always use a `WHERE` clause with `UPDATE`. If you don't, the database will update **every single row** in the table with the new content.

```sql
/* After user submitted their new diary log */
INSERT INTO diary_logs (user_id, date, content) VALUES (1, "2015-04-01",
    "I had a horrible fight with OhNoesGuy and I buried my woes in 3 pounds of dark chocolate.");

/* The user wants to admit they ate too much chocolate, so they update the log: */
UPDATE diary_logs SET content = "I had a horrible fight with OhNoesGuy" WHERE id = 1;
```

**Why use IDs?**
While you could filter by `user_id` or `date`, using the **Primary Key (ID)** is the safest method. It ensures you target exactly one unique row, even if a user has multiple logs on the same day.

### 16.3 Deleting Records (DELETE)
If a user wants to remove an entry entirely, we use the `DELETE` command.

```sql
-- Deleting the specific log entry
DELETE FROM diary_logs WHERE id = 1;

-- Verify the deletion
SELECT * FROM diary_logs;
```

### 16.4 Industry Tip: Soft Deletes
In many professional applications, data is rarely "truly" deleted. Instead, developers use a **"Soft Delete"** strategy:
1.  Add a `deleted` column (Boolean) to the table.
2.  When a user "deletes" a row, run an `UPDATE` to set `deleted = TRUE`.
3.  Filter all `SELECT` queries to only show rows where `deleted = FALSE`.

This prevents accidental data loss and allows for data recovery if needed.

### 🏁 Chapter Summary
With `SELECT`, `INSERT`, `UPDATE`, and `DELETE`, you now have the "Big Four" commands (CRUD: Create, Read, Update, Delete) required to build almost any data-driven application!

---

## 17. Altering tables after creation
> 📚 **Purpose**: Demonstrate how to modify the structure of existing tables without losing data.
> 🎯 **Goal**: Evolve database schemas to accommodate new requirements using the ALTER command.

In a real production environment, you cannot simply edit a `CREATE TABLE` statement once it has been executed and data has been collected. Re-running a `CREATE` statement would typically require dropping the existing table, which causes the permanent loss of all user data. To modify a table's structure safely, we use the `ALTER TABLE` command.

### 17.1 Scenario: Evolving the Diary App
Imagine that a few months after launching the diary app, a designer suggests adding an emotion drop-down (Happy, Sad, Confused) to each entry. To store this, we need to add a new `emotion` column without deleting existing logs.

```sql
/* 1. Original Table Structure */
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT);
    
CREATE TABLE diary_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    date TEXT,
    content TEXT
    );
    
/* 2. Initial Data Entry */
INSERT INTO diary_logs (user_id, date, content) VALUES (1, "2015-04-02",
    "OhNoesGuy and I made up and now we're best friends forever and we celebrated with a tub of ice cream.");
    
/* 3. Modifying the Schema with ALTER TABLE */
-- We add 'emotion' with a default value to avoid NULLs in existing rows
ALTER TABLE diary_logs ADD emotion TEXT default "unknown";

/* 4. New Data Entry with the New Column */
INSERT INTO diary_logs (user_id, date, content, emotion) VALUES (1, "2015-04-03",
    "We went to Disneyland!", "happy");
    
/* 5. Verify the Change */
SELECT * FROM diary_logs;
```

### 17.2 Default Values vs. NULL
- **The NULL Problem**: If we added the column without a default, the first row (the ice cream celebration) would show `NULL` for emotion.
- **The DEFAULT Solution**: By specifying `default "unknown"`, the database automatically fills existing rows with that value, making it easier for the app to handle.

### 17.3 Deleting Tables (DROP TABLE)
You can remove an entire table using `DROP TABLE`. This is rarely done except during data migrations or testing.

**Warning**: This is a nuclear option. Once a table is dropped, all its data and its schema are gone forever. If you try to `SELECT` from it afterwards, you will get an error because the table no longer exists.

### ⚡ Safety & Performance
- **Performance**: Be careful running `ALTER TABLE` on tables with millions of rows, as it can cause significant performance lag.
- **Responsibility**: "With great power comes great responsibility." Always backup your data before making schema changes.

---

## 18. Database Administration & Safety
> 📚 **Purpose**: Discuss best practices for data security, backups, and access control.
> 🎯 **Goal**: Ensure the long-term reliability and protection of database systems.

### 18.1 Backups & Replication
Even with careful coding, hardware failures or human errors occur.
- **Backups**: Companies make hourly, daily, or weekly copies of the database. If data is lost, it can be imported from an older version.
- **Replication**: Storing multiple copies of the database in different physical locations. This ensures **Availability**—if one server is hit by lightning, queries are redirected to a surviving copy.

### 18.2 Granting Privileges (Access Control)
In professional environments (shared servers), access is controlled via users and privileges.
- **Principle of Least Privilege**: Only give users the minimum access they need.
    ```sql
    -- Full access for admins
    GRANT FULL ON TABLE users TO super_admin;

    -- Read-only access for analysts
    GRANT SELECT ON TABLE users TO analyzing_user;
    ```
- **Privacy**: Anonymized database versions are often used to allow analysis without exposing sensitive information like emails or names.

---

## 19. Next Steps
> 📚 **Purpose**: Define a clear progression path for continuing SQL and database education.
> 🎯 **Goal**: Transition from basic queries to advanced optimization and architectural design.

### Immediate Goals
- ✅ Practice CREATE TABLE and INSERT commands
- ✅ Learn SELECT, ORDER BY, and WHERE clauses
- ✅ Experiment with different WHERE conditions
- ✅ Understand data types and PRIMARY KEY
- ✅ Master IN, Subqueries, and LIKE
- ✅ Master CASE statements and math operators
- ✅ Master data manipulation (UPDATE/DELETE)
- ✅ Practice JOIN operations (Cross, Implicit, Explicit)
- ✅ Master OUTER JOINs (LEFT OUTER JOIN)
- ✅ Master Self Joins (Using Aliases)
- ✅ Master Combining Multiple Joins
- ✅ Learn aggregation functions
- ✅ Explore advanced query techniques

### Intermediate Goals
- Master UPDATE and DELETE commands
- Work with aggregation functions (COUNT, SUM, AVG)

### Advanced Goals
- Indexing and performance optimization
- Transaction management
- Stored procedures
- NoSQL database fundamentals

### Practice Projects
1. Build a personal expense tracker database
2. Create a book library database
3. Design a social network graph
4. Practice with real-world datasets

---

## 💡 Key Takeaways
> 📚 **Purpose**: Summarize the most critical concepts covered in the roadmap.
> 🎯 **Goal**: Reinforce essential knowledge for quick review and retention.

1. **Databases store data** in tables with rows and columns
2. **SQL queries** help you retrieve, modify, and analyze data
3. **Unique IDs** are essential for identifying rows
4. **ORDER BY** sorts results logically
5. **WHERE clauses** filter results efficiently
6. **Relational databases** link tables through IDs
7. **Practice with SQLite** to build hands-on skills

---

## 📝 Learning Progress
> 📚 **Purpose**: Provide a checklist for tracking advancement through the database roadmap.
> 🎯 **Goal**: Maintain a clear record of mastered topics and remaining learning goals.

- [x] Basics of DBMS and SQL
- [x] Database Development Lifecycle (DBLC)
- [x] Three Levels of Design (Conceptual, Logical, Physical)
- [x] Understanding Tables & Relationships
- [x] Primary, Foreign, and Composite Keys
- [x] Referential Integrity (Cascading)
- [x] Normalization (1NF, 2NF, 3NF)
- [x] Read vs Write Concepts
- [x] CREATE TABLE and INSERT commands
- [x] SELECT, ORDER BY, and WHERE clauses
- [x] IN, Subqueries, and LIKE
- [x] CASE statements and math operators
- [x] Aggregation functions (GROUP BY, HAVING)
- [x] UPDATE and DELETE commands
- [x] ALTER and DROP TABLE commands
- [x] JOINing Related Tables (Cross, Implicit, Explicit)
- [x] OUTER JOINs (LEFT, conceptual RIGHT/FULL)
- [x] Self Joins (Using Aliases & Self Outer Joins)
- [x] Combining Multiple Joins
- [x] Joins & Set Operations
- [ ] Indexes and optimization
- [ ] Advanced SQL topics

---

**Created**: 📅 2026-05-23
**Last Updated**: 📅 2026-06-12
**Version**: 3.0 (Milestone: Complex Multi-Joins Completed)
---

> 🚀 **Keep Learning**: SQL is essential for data science. Practice regularly and explore different use cases!
