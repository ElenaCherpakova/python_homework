# Task 3: Interactive Visualizations with Plotly

import plotly.express as px
import plotly.data as pldata

df = pldata.wind(return_type='pandas')
print(df.head(10))
print(df.tail(10))

def convert_strength_to_float(val):
    val = str(val).strip()
    if '-' in val:
        num1, num2 = val.split('-')
        return (float(num1) + float(num2)) / 2
    else:
        return float(val.replace('+', ''))
df['strength'] = df['strength'].apply(convert_strength_to_float)
fig = px.scatter(df, x='strength', y='frequency', color="direction",
                 title="strength vs. frequency")
fig.write_html("wind.html", auto_open=True)
