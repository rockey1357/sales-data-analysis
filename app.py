import os
from flask import Flask, render_template, request, redirect, session
import mysql.connector
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = "sales_project_secret"


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get("DB_PASSWORD", ""),
        database="sales_analysis"
    )
    return connection


# =========================
# LOGIN
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return render_template(
                "register.html",
                error="Passwords do not match"
            )

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            connection.close()
            return render_template(
                "register.html",
                error="Username already exists"
            )

        cursor.execute(
            "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
            (name, username, password)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================
# DASHBOARD
# =========================
@app.route("/")
def portal():
    return render_template("portal.html")



@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    df = pd.read_sql(
        "SELECT * FROM sales",
        connection
    )

    connection.close()

    if df.empty:

        total_sales = 0
        total_quantity = 0
        average_sales = 0
        best_product = "No Data"
        best_region = "No Data"
        growth = 0

    else:

        df["sales_amount"] = (
            df["quantity"] * df["price"]
        )

        total_sales = round(
            df["sales_amount"].sum(),
            2
        )

        total_quantity = int(
            df["quantity"].sum()
        )

        average_sales = round(
            np.mean(df["sales_amount"]),
            2
        )

        product_sales = df.groupby(
            "product_name"
        )["sales_amount"].sum()

        region_sales = df.groupby(
            "region"
        )["sales_amount"].sum()

        best_product = product_sales.idxmax()

        best_region = region_sales.idxmax()

        df["sale_date"] = pd.to_datetime(
            df["sale_date"]
        )

        monthly_sales = df.groupby(
            df["sale_date"].dt.to_period("M")
        )["sales_amount"].sum()

        growth = 0

        if len(monthly_sales) >= 2:

            previous_month = monthly_sales.iloc[-2]

            current_month = monthly_sales.iloc[-1]

            if previous_month != 0:

                growth = round(
                    (
                        (current_month - previous_month)
                        / previous_month
                    ) * 100,
                    2
                )

    return render_template(
        "dashboard.html",
        total_sales=total_sales,
        total_quantity=total_quantity,
        average_sales=average_sales,
        best_product=best_product,
        best_region=best_region,
        growth=growth
    )


# =========================
# SALES RECORDS
# =========================

@app.route("/sales")
def sales():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get(
        "search",
        ""
    )

    category = request.args.get(
        "category",
        ""
    )

    region = request.args.get(
        "region",
        ""
    )

    sort = request.args.get(
        "sort",
        ""
    )

    connection = get_db_connection()

    query = "SELECT * FROM sales WHERE 1=1"

    values = []

    if search:

        query += """
        AND (
            product_name LIKE %s
            OR customer_name LIKE %s
        )
        """

        search_value = "%" + search + "%"

        values.append(search_value)
        values.append(search_value)

    if category:

        query += " AND category = %s"

        values.append(category)

    if region:

        query += " AND region = %s"

        values.append(region)

    if sort == "price":

        query += " ORDER BY price DESC"

    elif sort == "quantity":

        query += " ORDER BY quantity DESC"

    elif sort == "date":

        query += " ORDER BY sale_date DESC"

    else:

        query += " ORDER BY sale_id DESC"

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute(
        query,
        values
    )

    sales_data = cursor.fetchall()

    cursor.close()

    connection.close()

    return render_template(
        "sales.html",
        sales=sales_data,
        search=search,
        category=category,
        region=region,
        sort=sort
    )


# =========================
# ADD SALE
# =========================

@app.route(
    "/add-sale",
    methods=["GET", "POST"]
)
def add_sale():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        sale_date = request.form["sale_date"]

        product_name = request.form[
            "product_name"
        ]

        category = request.form[
            "category"
        ]

        quantity = request.form[
            "quantity"
        ]

        price = request.form[
            "price"
        ]

        customer_name = request.form[
            "customer_name"
        ]

        region = request.form[
            "region"
        ]

        connection = get_db_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO sales
        (
            sale_date,
            product_name,
            category,
            quantity,
            price,
            customer_name,
            region
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        values = (
            sale_date,
            product_name,
            category,
            quantity,
            price,
            customer_name,
            region
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()

        return redirect("/sales")

    return render_template(
        "add_sale.html"
    )


# =========================
# EDIT SALE
# =========================

@app.route(
    "/edit-sale/<int:sale_id>",
    methods=["GET", "POST"]
)
def edit_sale(sale_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    if request.method == "POST":

        sale_date = request.form[
            "sale_date"
        ]

        product_name = request.form[
            "product_name"
        ]

        category = request.form[
            "category"
        ]

        quantity = request.form[
            "quantity"
        ]

        price = request.form[
            "price"
        ]

        customer_name = request.form[
            "customer_name"
        ]

        region = request.form[
            "region"
        ]

        query = """
        UPDATE sales
        SET
            sale_date=%s,
            product_name=%s,
            category=%s,
            quantity=%s,
            price=%s,
            customer_name=%s,
            region=%s
        WHERE sale_id=%s
        """

        values = (
            sale_date,
            product_name,
            category,
            quantity,
            price,
            customer_name,
            region,
            sale_id
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()

        connection.close()

        return redirect("/sales")

    cursor.execute(
        "SELECT * FROM sales WHERE sale_id=%s",
        (sale_id,)
    )

    sale = cursor.fetchone()

    cursor.close()

    connection.close()

    return render_template(
        "edit_sale.html",
        sale=sale
    )


# =========================
# DELETE SALE
# =========================

@app.route(
    "/delete-sale/<int:sale_id>"
)
def delete_sale(sale_id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM sales WHERE sale_id=%s",
        (sale_id,)
    )

    connection.commit()

    cursor.close()

    connection.close()

    return redirect("/sales")


# =========================
# IMPORT CSV
# =========================

@app.route(
    "/import-csv",
    methods=["GET", "POST"]
)
def import_csv():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        if "file" not in request.files:

            return "No file selected."

        file = request.files["file"]

        if file.filename == "":

            return "Please select a CSV file."

        if not file.filename.lower().endswith(
            ".csv"
        ):

            return "Only CSV files are allowed."

        try:

            df = pd.read_csv(file)

            required_columns = [
                "sale_date",
                "product_name",
                "category",
                "quantity",
                "price",
                "customer_name",
                "region"
            ]

            missing_columns = []

            for column in required_columns:

                if column not in df.columns:

                    missing_columns.append(
                        column
                    )

            if missing_columns:

                return (
                    "Missing columns: "
                    + ", ".join(
                        missing_columns
                    )
                )

            connection = get_db_connection()

            cursor = connection.cursor()

            imported = 0

            duplicates = 0

            errors = []

            for index, row in df.iterrows():

                row_number = index + 2

                try:

                    sale_date = pd.to_datetime(
                        row["sale_date"]
                    ).date()

                    product_name = str(
                        row["product_name"]
                    ).strip()

                    category = str(
                        row["category"]
                    ).strip()

                    quantity = int(
                        row["quantity"]
                    )

                    price = float(
                        row["price"]
                    )

                    customer_name = str(
                        row["customer_name"]
                    ).strip()

                    region = str(
                        row["region"]
                    ).strip()

                    if not product_name:

                        raise ValueError(
                            "Product name is empty"
                        )

                    if not category:

                        raise ValueError(
                            "Category is empty"
                        )

                    if not customer_name:

                        raise ValueError(
                            "Customer name is empty"
                        )

                    if not region:

                        raise ValueError(
                            "Region is empty"
                        )

                    if quantity <= 0:

                        raise ValueError(
                            "Quantity must be greater than 0"
                        )

                    if price <= 0:

                        raise ValueError(
                            "Price must be greater than 0"
                        )

                    duplicate_query = """
                    SELECT sale_id
                    FROM sales
                    WHERE sale_date=%s
                    AND product_name=%s
                    AND category=%s
                    AND quantity=%s
                    AND price=%s
                    AND customer_name=%s
                    AND region=%s
                    """

                    duplicate_values = (
                        sale_date,
                        product_name,
                        category,
                        quantity,
                        price,
                        customer_name,
                        region
                    )

                    cursor.execute(
                        duplicate_query,
                        duplicate_values
                    )

                    duplicate = cursor.fetchone()

                    if duplicate:

                        duplicates += 1

                        continue

                    insert_query = """
                    INSERT INTO sales
                    (
                        sale_date,
                        product_name,
                        category,
                        quantity,
                        price,
                        customer_name,
                        region
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """

                    cursor.execute(
                        insert_query,
                        duplicate_values
                    )

                    imported += 1

                except Exception as e:

                    errors.append(
                        "Row "
                        + str(row_number)
                        + ": "
                        + str(e)
                    )

            connection.commit()

            cursor.close()

            connection.close()

            return render_template(
                "import_csv.html",
                imported=imported,
                duplicates=duplicates,
                errors=errors,
                completed=True
            )

        except Exception as e:

            return (
                "Error processing CSV: "
                + str(e)
            )

    return render_template(
        "import_csv.html",
        completed=False
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)