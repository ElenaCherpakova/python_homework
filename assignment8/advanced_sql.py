import pandas as pd
import sqlite3
import traceback
from datetime import datetime

# Task 1 Complex JOINs with Aggregation
try:
    with sqlite3.connect('../db/lesson.db') as conn:
        sql_statement = """SELECT o.order_id, SUM(p.price * l.quantity) AS total_price FROM orders AS o 
        JOIN line_items AS l ON o.order_id = l.order_id
        JOIN products AS p ON l.product_id = p.product_id
        GROUP BY o.order_id
        ORDER BY o.order_id
        LIMIT 5;"""
        df = pd.read_sql_query(sql_statement, conn)
        print(df)

# Task 2: Understanding Subqueries
        sql_statement = """SELECT c.customer_name, 
        AVG(subquery.total_price) AS average_price FROM customers AS c
        LEFT JOIN (
            SELECT customer_id AS customer_id_b, 
            SUM(p.price * l.quantity) AS total_price, 
            o.order_id FROM orders AS o 
            JOIN line_items AS l ON o.order_id = l.order_id
            JOIN products AS p ON p.product_id = l.product_id
            GROUP BY o.customer_id, o.order_id) AS subquery 
        ON c.customer_id = subquery.customer_id_b
        GROUP BY c.customer_id;"""
        df = pd.read_sql_query(sql_statement, conn)
        print(df)

# Task 4: Aggregation with HAVING
        sql_statement = """SELECT e.first_name, e.last_name, COUNT(o.order_id) AS count_of_order FROM employees as e 
        JOIN orders as o ON e.employee_id = o.employee_id GROUP BY o.employee_id
        HAVING COUNT(o.order_id) > 5;"""
        df = pd.read_sql_query(sql_statement, conn)
        print(df)
except Exception as e:
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(
            f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
    print(f"An exception occurred. Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")

# Task 3: An Insert Transaction Based on Data


def find_customer_and_employee(cursor, customer_name, employee_name):
    first_name, last_name = employee_name.split(
        ' ')[0], employee_name.split(' ')[1]
    cursor.execute(
        "SELECT customer_id FROM customers WHERE customer_name = ?", (customer_name,))
    results = cursor.fetchall()
    if len(results) > 0:
        customer_id = results[0][0]
    else:
        print(f"There is no a customer named {customer_name}.")
        return

    cursor.execute(
        "SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?",
        (first_name, last_name))
    results = cursor.fetchall()
    if len(results) > 0:
        employee_id = results[0][0]
    else:
        print(
            f"There is no a employee named {employee_name}.")
        return
    cursor.execute(
        "SELECT product_id, price FROM products ORDER BY price ASC LIMIT 5")
    results = cursor.fetchall()
    if len(results) > 0:
        products_id = [product_id[0] for product_id in results]
    else:
        print(
            f"There are no products.")
        return
    return customer_id, employee_id, products_id


def insert_order(cursor, customer_id, employee_id):
    date = datetime.now().isoformat()
    sql_statement = """INSERT INTO orders (customer_id, employee_id, date) VALUES (?, ?, ?)
    RETURNING order_id"""

    try:
        cursor.execute(sql_statement, (customer_id, employee_id, date))
        results = cursor.fetchall()
        if len(results) > 0:
            order_id = results[0][0]
            print(f"Order {order_id} added successfully.")
            return order_id
        else:
            print("No order was added.")
            return None
    except sqlite3.IntegrityError:
        print(f"Order for {customer_id} is already in database.")


def insert_into_line_items(cursor, order_id, products_id):
    sql_statement = """INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?)"""
    quantity = 10
    try:
        for product_id in products_id:
            cursor.execute(sql_statement, (order_id, product_id, quantity))
        print(f"Line items for {order_id} added successfully.")
    except sqlite3.IntegrityError:
        print(f"Line items for {order_id} is already in database.")


def check_inserted_order(cursor, order_id):
    sql_statement = """SELECT l.line_item_id, p.product_name, l.quantity FROM line_items AS l
    JOIN products AS p ON l.product_id = p.product_id
    WHERE l.order_id = ?"""
    try:
        cursor.execute(sql_statement, (order_id,))
        results = cursor.fetchall()
        if len(results) > 0:
            df = pd.DataFrame(results, columns=[
                              'line_item_id', 'product_name', 'quantity'])
            print(f"Line items for order {order_id}:\n{df}")
            return df
        else:
            print(f"There are no line items for {order_id}.")
            return None
    except Exception as e:
        print(f"An error occurred while checking inserted order: {e}")
        return None


def delete_by_order_id(cursor, order_id):
    sql_line_items = """DELETE FROM line_items WHERE order_id = ?"""
    sql_orders = """DELETE FROM orders WHERE order_id = ?"""
    try:
        cursor.execute(sql_line_items, (order_id,))
        print(f"Line items for order {order_id} deleted successfully.")
        cursor.execute(sql_orders, (order_id,))
        print(f"Order {order_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Failed to delete order {order_id} and line items: {e}")


try:
    with sqlite3.connect('../db/lesson.db') as conn:
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = 1")
        # Insert sample data into tables
        customer_id, employee_id, product_ids = find_customer_and_employee(
            cursor, 'Perez and Sons', 'Miranda Harris')
        order_id = insert_order(cursor, customer_id, employee_id)
        insert_into_line_items(cursor, order_id, product_ids)

        check_by_inserted_order_id = check_inserted_order(cursor, order_id)
        deleting = delete_by_order_id(cursor, order_id)

        conn.commit()

except sqlite3.Error as e:
    conn.rollback()
    print(f"An error occurred: {e}")
