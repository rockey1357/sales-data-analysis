# Sales Data Analysis System

## 1. Project Overview

The Sales Data Analysis System is a web-based application developed using Python, Flask, MySQL, Pandas, NumPy and Matplotlib.

The system helps users store, manage and analyze sales records. It provides a colorful dashboard that displays important sales information and charts.

## 2. Technologies Used

* Python
* Flask
* MySQL
* Pandas
* NumPy
* Matplotlib
* HTML
* CSS

## 3. Main Features

* View sales records
* Add new sales
* Edit existing sales
* Delete sales
* Search sales
* Filter sales by category
* Filter sales by region
* Calculate total sales
* Calculate total quantity
* Calculate average sales
* Find best-selling product
* Find best-performing region
* Display sales charts
* Input validation
* Error handling

## 4. Project Structure

```text
sales_data_analysis/
│
├── app.py
├── charts.py
├── README.md
│
├── templates/
│   ├── dashboard.html
│   ├── sales.html
│   ├── add_sale.html
│   └── edit_sale.html
│
└── static/
    ├── monthly_sales.png
    ├── product_sales.png
    └── region_sales.png
```

## 5. Database

Database Name:

```text
sales_analysis
```

Table Name:

```text
sales
```

The sales table contains:

* Sale ID
* Sale Date
* Product Name
* Category
* Quantity
* Price
* Customer Name
* Region

## 6. How to Run the Project

Open PowerShell in the project folder.

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the Flask application:

```powershell
python app.py
```

Open the following address in a browser:

```text
http://127.0.0.1:5000/
```

## 7. Dashboard

The dashboard displays:

* Total Sales
* Total Quantity
* Average Sales
* Best Product
* Best Region
* Monthly Sales Chart
* Product Sales Chart
* Region Sales Chart

## 8. CRUD Operations

The system supports CRUD operations:

### Create

Users can add new sales records.

### Read

Users can view all sales records.

### Update

Users can edit existing sales records.

### Delete

Users can delete sales records.

## 9. Search and Filtering

Users can search sales using:

* Product name
* Customer name

Users can also filter records using:

* Category
* Region

## 10. Validation

The system checks that:

* Required fields are filled.
* Quantity is greater than zero.
* Price is greater than zero.
* Quantity contains a valid number.
* Price contains a valid number.

## 11. Future Scope

The project can be improved in the future by adding:

* User login and authentication
* Export sales data to Excel or PDF
* More advanced charts
* Monthly and yearly reports
* Profit analysis
* Customer analysis
* Cloud database support
* Online deployment

## 12. Conclusion

The Sales Data Analysis System provides a simple and user-friendly way to manage and analyze sales data.

The combination of Flask, MySQL, Pandas, NumPy and Matplotlib makes it possible to store data, perform analysis and display useful information through an interactive web dashboard.

## 13. Database Password Setup

The MySQL password is not stored in the code. Set it before running:

```powershell
$env:DB_PASSWORD = "your_mysql_password"
python app.py
```

Install the required packages with:

```powershell
pip install -r requirements.txt
```
