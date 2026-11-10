# Sales Data Analysis System

## 1. Project Overview

A web-based application built with Python, Flask, MySQL, Pandas, NumPy and Matplotlib.
It helps users store, manage and analyze sales records, and shows the results on a dashboard with charts.

## 2. Technologies Used

* Python
* Flask
* MySQL
* Pandas
* NumPy
* Matplotlib
* HTML and CSS

## 3. Main Features

* User registration and login
* Add, view, edit and delete sales records (CRUD)
* Search by product or customer name
* Filter by category and region
* Import sales from a CSV file (with validation and duplicate check)
* Dashboard with total sales, total quantity, average sales, best product and best region
* Charts: monthly, product, region and category sales
* Input validation and error handling

## 4. Project Structure

```text
sales_data_analysis/
├── app.py              Flask application (routes, login, CRUD, CSV import)
├── analysis.py         Console analysis with Pandas and NumPy
├── charts.py           Creates the chart images in static/
├── database.sql        Database and table setup
├── requirements.txt    Python packages
├── test_sales.csv      Sample CSV (valid data)
├── test_invalid.csv    Sample CSV (invalid data for testing validation)
├── templates/          HTML pages (portal, login, register, dashboard, sales, add, edit, import)
└── static/             Chart images
```

## 5. Database

Database: `sales_analysis`

Tables:

* `users` (user_id, name, username, password)
* `sales` (sale_id, sale_date, product_name, category, quantity, price, customer_name, region)

## 6. How to Run

1. Install MySQL Server. Open the MySQL Command Line Client, log in, and create the database and tables:

```text
source C:/path/to/sales_data_analysis/database.sql;
```

2. Create a virtual environment and install packages (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Set the MySQL password (it is not stored in the code):

```powershell
$env:DB_PASSWORD = "your_mysql_password"
```

4. Start the app:

```powershell
python app.py
```

5. Open `http://127.0.0.1:5000/`, register a user and log in.

## 7. Validation

The system checks that:

* Required fields are filled.
* Quantity and price are valid numbers greater than zero.
* Duplicate sales are skipped during CSV import.
* Invalid CSV rows are rejected.

## 8. Future Scope

* Password hashing
* Export sales data to Excel or PDF
* More advanced charts and reports
* Profit and customer analysis
* Online deployment
