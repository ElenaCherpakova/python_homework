import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Task 2: A Line Plot with Pandas


def cumulative(row):
    totals_above = df['total_price'][0:row.name+1]
    return totals_above.sum()


try:
    with sqlite3.connect('../db/lesson.db') as conn:
        sql_statement = """
        SELECT o.order_id, SUM(price * quantity) AS total_price 
        FROM orders o JOIN employees e ON e.employee_id = o.employee_id JOIN line_items l ON o.order_id = l.order_id JOIN products p ON l.product_id = p.product_id GROUP BY o.order_id;
        """
        df = pd.read_sql_query(sql_statement, conn)
        df['cumulative'] = df.apply(cumulative, axis=1)
        # df['cumulative'] = df['total_price'].cumsum()
        df.plot(x='order_id', y='cumulative', kind='line',
                color='skyblue', title='cumulative revenue vs. order_id')
        plt.xlabel('Order Id')
        plt.ylabel('Cumulative Revenue')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

except sqlite3.Error as e:
    print(f"SQL Error: {e}")