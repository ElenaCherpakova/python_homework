import pandas as pd
import sqlite3
import traceback

try:
    with sqlite3.connect("../db/lesson.db") as conn:
        sql_statement = """SELECT l.line_item_id, l.quantity, p.product_id, p.product_name, p.price FROM line_items AS l JOIN products AS p ON l.product_id = p.product_id;""";
        df = pd.read_sql_query(sql_statement, conn)
        print('Initial DataFrame first 5 rows:')
        print(df.head())
        df['total'] = df['quantity'] * df['price']
        print('DataFrame after adding total column:')
        print(df.head())
        grouped = df.groupby('product_id').agg({'line_item_id': 'count', 'total': 'sum', 'product_name': 'first'}).head()
        grouped_sorted = grouped.sort_values(by='product_name')
        print('Grouped and sorted DataFrame:')
        print(grouped_sorted.head())

        grouped_sorted.to_csv('./order_summary.csv')
        print('Written to csv successfully.')
        
except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"An exception occurred. Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")       