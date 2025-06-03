import pandas as pd

df = pd.read_csv('../csv/employees.csv')
employee_names = [row["first_name"] + ' ' + row["last_name"] for index, row in df.iterrows()]
print(f"Employee Names: {employee_names}")

print("==========#============")
employee_contain_letter_e = [name for name in employee_names if 'e' in name]
print(f"Employee Names that contain letter e: {employee_contain_letter_e}")
