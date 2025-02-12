import dash
import pandas as pd
from dash import dcc, html
import dash.dash_table as dash_table
from dash.dependencies import Input, Output

# Google Sheets link (convert to CSV format)
sheet_url = "https://docs.google.com/spreadsheets/d/1pdThWZw8-KHaDnwP2gxLWpYsC5Y6HqLnzQYMea5hKNs/export?format=csv"

# Fetch data from Google Sheets
df = pd.read_csv(sheet_url)

# Strip any extra spaces in column names
df.columns = df.columns.str.strip()

# Clean data (replace NaN values with empty strings)
df = df.fillna("")

# Columns to display
columns_to_show = [
    'Total Registered', 'Visitors', 'Applied to Job', 'Application',
    'Unique Applicant', 'Total Companies Jobs Apply', 
    'Direct Payment for Job Apply', 'Paid by Applicants', 
    'Became Pro User Today', 'Amount from Today\'s Pro Users', 
    'Pro Job Seeker Count (apply jobs)', 'Total Amount Collected'
]

# Get the last row of the dataframe
last_row = df[columns_to_show].iloc[[-1]]  # Select only the last row with specific columns

# Transform data into a column-wise format
column_wise_data = [{'Attribute': col, 'Value': last_row[col].values[0]} for col in last_row.columns]

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with a fixed image header and DataTable to show the column-wise data
app.layout = html.Div([  
    html.Div([  
        # Logo on the left  
        html.Img(src='https://bdjobs.com/JobFair/it-job-fair-2025/bdjobs-chakri-mela-feb-2025.svg', 
                 style={'height': '100px', 'float': 'left', 'maxWidth': '100%', 'height': 'auto'}),  
        # Title centered with flexbox and auto margins for centering  
        html.H1('IT JobFair 2025', style={'textAlign': 'center', 'margin': '0 auto', 'fontSize': '3vw'}),  
    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),  

    # DataTable displaying the data in column-wise format  
    dash_table.DataTable(  
        id='data-table',  
        columns=[{"name": col, "id": col} for col in ['Attribute', 'Value']],  # Two columns: Attribute and Value  
        data=column_wise_data,  # Data in column-wise format  
        style_table={'height': 'auto', 'width': '60%', 'margin': 'auto'},  
        style_cell={'textAlign': 'center', 'fontSize': '16px'},  
        style_header={'backgroundColor': '#4F5D75', 'color': 'white'},  
        style_data={'backgroundColor': '#2B3B4B', 'color': 'white'}  
    ),  

    # Auto-refresh every 30 seconds  
    dcc.Interval(  
        id='interval-component',  
        interval=30*1000,  # 30 seconds  
        n_intervals=0  
    )  
])  

# Update table with new data periodically
@app.callback(  
    Output('data-table', 'data'),  
    Input('interval-component', 'n_intervals')  
)  
def update_data(n):  
    new_df = pd.read_csv(sheet_url).fillna("")  
    # Strip spaces and get the last row with specific columns  
    new_df.columns = new_df.columns.str.strip()  

    last_row = new_df[columns_to_show].iloc[[-1]]  # Get the last row of the updated data with selected columns  
    
    # Transform data into a column-wise format  
    column_wise_data = [{'Attribute': col, 'Value': last_row[col].values[0]} for col in last_row.columns]  
    
    return column_wise_data  
server = app.server
# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
