A web-based database management interface built with Python, Flask, and MySQL for the `shoestoredb` database (CSE 3330 — Project Phase 3). 

## Features

- **Employee Directory Lookup:** Queries employees hired on or after a selected date, joining `EMPLOYEE` and `DEPARTMENT` records to display employee ID, full name, hire date, department name, and floor number.
- **Register New Customer:** Inserts a new customer record (`Customer_ID`, `Fname`, `Lname`, `Phone`, `Email`) into the `CUSTOMER` table using parameterized SQL statements.
- **Update Customer Email:** Updates an existing customer's email address by `Customer_ID` and retrieves the updated row for immediate verification.
- **Remove Customer Record:** Deletes a customer record from the `CUSTOMER` table by `Customer_ID` with row-count verification.

## Tech Stack

- **Backend:** Python 3, Flask
- **Database:** MySQL (`shoestoredb`)
- **Database Driver:** `mysql-connector-python`
- **Frontend:** HTML5
