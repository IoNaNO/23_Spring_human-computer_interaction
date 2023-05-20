import dash
from dash import dcc, html
from dash.dependencies import State, Input, Output
import plotly.express as px
import pandas as pd

app=dash.Dash(
    __name__,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0,maximum-scale=1.2, minimum-scale=0.5,user-scalable=no",
        }
    ])

app.title="College Salaries Visualization"
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

# Read csv from dataset
df=pd.read_csv('./dataset/processed/salaries-by-region-geocoded.csv')
df2=pd.read_csv('./dataset/college-salaries/salaries-by-college-type.csv')
df3=pd.read_csv('./dataset/college-salaries/degrees-that-pay-back.csv')
salary_cols = ['Starting Median Salary', 'Mid-Career Median Salary', 
                   'Mid-Career 10th Percentile Salary', 'Mid-Career 25th Percentile Salary',
                   'Mid-Career 75th Percentile Salary', 'Mid-Career 90th Percentile Salary']

# Convert salary to float
def convert_salary(salary):
    if type(salary) == float or type(salary) == int:
        return salary
    try:
        # remove any special characters like commas and dollar signs
        salary = salary.replace(',', '').replace('$', '')
        return float(salary)
    except ValueError:
        return None

df['Starting Median Salary'] = df['Starting Median Salary'].apply(convert_salary)
df2['Mid-Career 90th Percentile Salary']=df2['Mid-Career 90th Percentile Salary'].apply(convert_salary)
df3[salary_cols]=df3[salary_cols].applymap(convert_salary)

# Render map graph
def render_map():
    return dcc.Graph(
        id='salary-map',
        figure=px.scatter_mapbox(df, lat='lat', lon='lon', hover_name='School Name', hover_data=['Starting Median Salary', 'Mid-Career Median Salary', 'Mid-Career 10th Percentile Salary', 'Mid-Career 25th Percentile Salary', 'Mid-Career 75th Percentile Salary', 'Mid-Career 90th Percentile Salary'],size='Starting Median Salary', color='Region', zoom=3, height=800).update_layout(mapbox_style='open-street-map', mapbox_accesstoken=mapbox_access_token)
    )

# Render bar graph
@app.callback(
    Output('salary-bar', 'figure'),
    [Input('dropdown', 'value')]
)
def render_bar(school_type):
    filtered_df = df2[df2['School Type'] == school_type]
    top5=filtered_df.nlargest(5,'Mid-Career 90th Percentile Salary')
    fig=px.bar(top5,y='School Name',x='Mid-Career 90th Percentile Salary',title=f'Top 5 {school_type} Colleges with Highest Mid-Career 90th Percentile Salary')
    fig.update_layout(
        yaxis=dict(autorange="reversed"))
    return fig

# Render line graph
@app.callback(
    Output('salary-line', 'figure'),
    [Input('major-dropdown', 'value')]
)
def render_line(selected_major):
    filtered_df = df3[df3['Undergraduate Major'] == selected_major]
    wage_values = filtered_df.loc[filtered_df['Undergraduate Major'] == selected_major, salary_cols].values[0]
    data_for_graph = pd.DataFrame({'Stage': salary_cols, 'Salaries': wage_values})
    fig = px.line(data_for_graph, x='Stage', y='Salaries', title=f'{selected_major} Salaries by Career Stage')
    return fig

# Web layout
app.layout=html.Div([
    html.Div(
        children=[
            html.H1(children='College Salaries Visualization')
        ]
    ),
    html.Div([
        html.H2(children='Map of College Salaries',style={"display": "flex", "align-items": "center","margin":"0 20px 20px 0"}),
        html.Div(
            render_map(),
            style={"display": "inline-block","width":"98%", "align-items": "center","justify-content":"center","margin":"1% 20px 20px 1%"}
        )
    ],
        # style={
        #     "background-color": "#f8f8f8",
        #     'borderBottom': 'thin lightgrey solid',
        # }
    ),
    html.Div([
        html.H2(children='Details of College Salaries',style={"display": "flex", "align-items": "center","margin":"0 20px 20px 0"}),
        html.Div([
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': i, 'value': i} for i in df2['School Type'].unique()],
                value='Engineering',    # default choice
            ),
            dcc.Graph(id='salary-bar')
        ],
            style={'width': '49%', 'display': 'inline-block'}        
        ),
        html.Div([
            dcc.Dropdown(
                id='major-dropdown',
                options=[{'label': i, 'value': i} for i in df3['Undergraduate Major'].unique()],
                value='Accounting',    # default choice
            ),
            dcc.Graph(id='salary-line')
        ],
            style={'width': '49%', 'display': 'inline-block', 'float': 'right'}        
        )
    ]),
])

if __name__=='__main__':
    app.run(debug=True)