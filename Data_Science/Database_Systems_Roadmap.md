# 🗺️ Database Systems Roadmap: A Learning Guide

> 📚 **Purpose**: A structured guide for learning about database systems, SQL, and data science fundamentals.
> 
> 🎯 **Goal**: Build a solid foundation in databases and SQL for data science applications.

---

## 📋 Table of Contents

1. [What is a DBMS?](#1-what-is-a-database-management-system)
2. [Intro to SQL & Data](#2-intro-to-sql--data)
3. [Understanding Tables & Relationships](#3-understanding-tables--relationships)
4. [🗣️ SQL Basics: CREATE & INSERT](#sql-basics-create--insert)
5. [SQL Queries: SELECT, ORDER BY, WHERE](#sql-queries-select-order-by-where)
6. [Roles in the Ecosystem](#roles-in-the-ecosystem)
7. [Tools & Resources](#tools--resources)
8. [Next Steps](#next-steps)

---

## 1. What is a DBMS?

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

---

## 2. Intro to SQL & Data

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

### Data Structure Examples

```sql
-- User Data Example
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    nickname TEXT,
    location TEXT
);

CREATE TABLE badges (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE user_badges (
    user_id INTEGER,
    badge_id INTEGER
);
```

### Why Unique IDs Matter
- **Identify rows**: Find specific records to update/delete
- **Avoid dependencies**: Don't rely on changing columns
- **Standard practice**: `id` column first, declared as `INTEGER PRIMARY KEY`

### Table Relationships
- One-to-Many: Users ↔ Badges
- Many-to-Many: Via junction table (`user_badges`)
- Efficient storage: Store IDs, not repeated data

---

## 🗣️ SQL Basics: CREATE & INSERT

### Creating Your First Table

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
```

---

## SQL Queries: SELECT, ORDER BY, WHERE

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

## Roles in the Ecosystem

| Role | Responsibility |
|------|----------------|
| **Data Modeler** | Designs data structure and relationships |
| **Database Administrator (DBA)** | Maintains database, ensures security |
| **Backend Developer** | Builds API, connects apps to data |
| **Data Analyst** | Uses SQL for analysis and reporting |
| **Data Scientist** | Advanced analytics, machine learning |

---

## Tools & Resources

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

-- Filter with condition
SELECT * FROM customers WHERE age > 21;

-- Filter with multiple conditions
SELECT * FROM customers WHERE age < 21 AND state = "NY";

-- Filter with IN
SELECT * FROM customers WHERE plan IN ("free", "basic");

-- Select specific columns
SELECT name, age FROM customers;

-- Order results
SELECT name, age FROM customers ORDER BY age DESC;

-- Transform with CASE
SELECT name, CASE WHEN age > 18 THEN "adult" ELSE "minor" END AS type FROM customers;

-- See also: filtering with LIKE, restricting with LIMIT, using ROUND and other core functions
-- For more details: SQLite reference for SELECT
```

### Aggregating Data
```sql
-- Aggregate functions
SELECT MAX(age) FROM customers;

-- Grouping data
SELECT gender, COUNT(*) FROM students GROUP BY gender;

-- See also: restricting results with HAVING
```

### Joining Related Tables
```sql
-- Joining related tables
SELECT customers.name, orders.item FROM customers JOIN orders ON customers.id = orders.customer_id;

-- Inner join
SELECT customers.name, orders.item FROM customers LEFT OUTER JOIN orders ON customers.id = orders.customer_id;

-- Outer join (LEFT OUTER JOIN returns all rows from left table, even if no match in right table)
```

### Updating and Deleting Data
```sql
-- Updating data
UPDATE customers SET age = 33 WHERE id = 73;

-- Deleting data
DELETE FROM customers WHERE id = 73;
```

---

## Next Steps

### Immediate Goals
- ✅ Practice CREATE TABLE and INSERT commands
- ✅ Learn SELECT, ORDER BY, and WHERE clauses
- ✅ Experiment with different WHERE conditions
- ✅ Understand data types and PRIMARY KEY
- ✅ Master data manipulation (UPDATE/DELETE)
- ✅ Practice JOIN operations
- ✅ Learn aggregation functions
- ✅ Explore advanced query techniques

### Intermediate Goals
- Learn JOIN operations
- Master UPDATE and DELETE commands
- Practice with subqueries
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

1. **Databases store data** in tables with rows and columns
2. **SQL queries** help you retrieve, modify, and analyze data
3. **Unique IDs** are essential for identifying rows
4. **ORDER BY** sorts results logically
5. **WHERE clauses** filter results efficiently
6. **Relational databases** link tables through IDs
7. **Practice with SQLite** to build hands-on skills

---

## 📝 Learning Progress

- [x] Basics of DBMS and SQL
- [x] CREATE TABLE and INSERT commands
- [x] SELECT, ORDER BY, and WHERE clauses
- [ ] JOIN operations
- [ ] UPDATE and DELETE commands
- [ ] Subqueries and aggregation
- [ ] Indexes and optimization
- [ ] Advanced SQL topics

---

**Created**: 📅 [Current Date]
**Last Updated**: 📅 [Current Date]
**Version**: 2.0

---

> 🚀 **Keep Learning**: SQL is essential for data science. Practice regularly and explore different use cases!
