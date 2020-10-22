from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app

layout = html.Div([
    html.Div([
        dcc.Markdown("""### Explanation""")
    ], style={'textAlign': 'center'}),
    html.Div([
        dcc.Markdown("""
        When I was first making the prediction model, I chose to do a `RandomForestRegressor` for predicting movie runtimes. I passed in my data and it showed a 8.5 minute MAE. I realized I had fit the model wrong and was using all my data and not just training data. After I had fit just the training data and tested on the validation data, the model was complete and utter horse doodoo. The model only increased accuracy by about .3 minutes from the baseline of 20.2 minutes to 19.9 minutes. 
        
        I chose a ridge model to test next. That had pretty much the same accuracy \(that's the model doing the predicting btw\), so my theory is that I don't have good/enough features to accurately predict a movies runtime. I personally think that there are a lot of features that don't really help in predicting the runtime of movies.

        I could look for more features/info about movies in order to predict runtime, which might help. Here are the feature coefficients of the current model.
        """),
        html.Img(src=app.get_asset_url('ridge_importance.jpg'))
    ])
])
