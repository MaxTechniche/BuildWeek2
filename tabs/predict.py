from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from joblib import load
import numpy as np
import pandas as pd

from app import app

loan_purposes = ['Business',
                 'Car financing',
                 'Credit card refinancing',
                 'Debt consolidation',
                 'Green loan',
                 'Home buying',
                 'Home improvement',
                 'Major purchase',
                 'Medical expenses',
                 'Moving and relocation',
                 'Other',
                 'Vacation']

style = {'padding': '1.5em'}

layout = html.Div([
    dcc.Markdown("""
        ### Predict

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
    
    """), 

    html.Div([
        dcc.Markdown('###### Annual Income'), 
        dcc.Slider(
            id='annual-income', 
            min=20000,
            max=200000,
            step=5000,
            value=65000, 
            marks={n: f'{n/1000:.0f}k' for n in range(20000,220000,20000)} 
        ), 
    ], style=style), 

    html.Div([
        dcc.Markdown('###### Credit Score'), 
        dcc.Slider(
            id='credit-score', 
            min=650,
            max=850, 
            step=10, 
            value=700, 
            marks={n: str(n) for n in range(650,900,50)}
        ),
    ], style=style), 

    html.Div([
        dcc.Markdown('###### Loan Amount'), 
        dcc.Slider(
            id='loan-amount', 
            min=1000, 
            max=40000, 
            step=1000, 
            value=10000, 
            marks={n: f'{n/1000:.0f}k' for n in range(5000,45000,5000)}
        ),  
    ], style=style),

    html.Div([
        dcc.Markdown('###### Loan Purpose'), 
        dcc.Dropdown(
            id='loan-purpose', 
            options=[{'label': purpose, 'value': purpose} for purpose in loan_purposes], 
            value=loan_purposes[0]
        ), 
    ], style=style),

    html.Div([
        dcc.Markdown('###### Monthly Debts'), 
        dcc.Slider(
            id='monthly-debts', 
            min=0, 
            max=5000, 
            step=100, 
            value=1000, 
            marks={n: str(n) for n in range(500,5500,500)}
        )
    ], style=style),

    dcc.Markdown('### Prediction'), 
    html.Div(id='prediction-content', style={'marginBottom': '5em'}), 

])

@app.callback(
    Output('prediction-content', 'children'),
    [Input('annual-income', 'value'),
     Input('credit-score', 'value'),
     Input('loan-amount', 'value'),
     Input('loan-purpose', 'value'),
     Input('monthly-debts', 'value')])
def predict(annual_income, credit_score, loan_amount, loan_purpose, monthly_debts):

    df = pd.DataFrame(
        columns=['Annual Income', 'Credit Score', 'Loan Amount', 'Loan Purpose', 'Monthly Debts'], 
        data=[[annual_income, credit_score, loan_amount, loan_purpose, monthly_debts]]
    )

    pipeline = load('model/pipeline.joblib')
    y_pred_log = pipeline.predict(df)
    y_pred = np.expm1(y_pred_log)[0]

    return f'Interest rate for 36 month loan: {y_pred:.2f}%'
