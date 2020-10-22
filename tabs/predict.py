from dash.dependencies import Input, Output
import dash_core_components as dcc
from dash_core_components.Markdown import Markdown
from dash_core_components.Textarea import Textarea
import dash_html_components as html

from joblib import load
import numpy as np
import pandas as pd
from sklearn.utils.validation import column_or_1d

from app import app

genres = ['Mystery', 'War', 'Sci-Fi', 'Animation', 'Western',
    'Biography', 'Action', 'Thriller', 'Comedy', 'Music', 'Romance',
    'Musical', 'Family', 'Crime', 'Sport', 'Adventure', 'Film-Noir',
    'Fantasy', 'Drama', 'Horror', 'History'
]

certifications = ['R', 'PG-13', 'Approved', 'PG', 'Not Rated', 'G', 'Passed', 'TV-14', 'GP', 'TV-PG', 'TV-MA', 'Unrated', 'NC-17', 'M']

style = {'padding': '.5em', 'paddingLeft': '1.5em', 'margin': '.1em'}

layout = html.Div([
    dcc.Markdown("""
        ### Predict Movie Runtime
    
    """),
    html.Div(id='prediction-content', style={'marginBottom': '0em', **style, 'paddingLeft': '27em'}), 

    html.Div([
        dcc.Markdown('###### Title'), 
        dcc.Input(
            id='title',
            type='text',
            placeholder='Title...' 
        ),
    ], style=style), 

    html.Div([
        dcc.Markdown('###### Year'), 
        dcc.Input(
            id='year',
            type='number',
            placeholder='Year...' 
        ),
    ], style=style), 

    html.Div([
        dcc.Markdown('###### Certification'), 
        dcc.Dropdown(
            id='certification', 
            options=[{'label': cert, 'value': cert} for cert in certifications]
        ), 
    ], style={'width': '19%', **style}),

    html.Div([
        dcc.Markdown('###### User Rating'),
        dcc.Slider(
            id='rating',
            min=0,
            max=10,
            step=.1,
            # value=5,
            marks={n: str(n) for n in range(0,11,1)}
        )
    ], style=style),

    html.Div([
        dcc.Markdown('###### Metascore'), 
        dcc.Slider(
            id='metascore', 
            min=0, 
            max=100, 
            step=1, 
            # value=50, 
            marks={n: str(n) for n in range(0,101,5)}
        )
    ], style=style),

    html.Div([
        dcc.Markdown('###### USA Box Office'), 
        dcc.Slider(
            id='usa_box_office', 
            min=0, 
            max=1000000000, 
            step=100000, 
            # value=500000000, 
            marks={n: str(n)[:-6]+'M' for n in range(0,1000000001,100000000)}
        )
    ], style=style),

    html.Div([
        dcc.Markdown('###### Number of Votes'), 
        dcc.Slider(
            id='votes', 
            min=0, 
            max=3000000, 
            step=100, 
            #value=1500000, 
            marks={n: str(n)[:-3]+'K' for n in range(0,3000001,500000)}
        )
    ], style=style),

    html.Div([
        dcc.Markdown('###### Genres'), 
        dcc.Dropdown(
            id='genres', 
            options=[{'label': genre, 'value': genre} for genre in genres], 
            multi=True
        ), 
    ], style={'width': '40%', **style}),

    html.Div([
        dcc.Markdown('###### Movie Description'),
        dcc.Textarea(
            id='description',
            style={'width': '100%'}
        )
    ], style=style),


])

@app.callback(
    Output('prediction-content', 'children'),
    [Input('title', 'value'),
     Input('year', 'value'),
     Input('certification', 'value'),
     Input('rating', 'value'),
     Input('metascore', 'value'),
     Input('usa_box_office', 'value'),
     Input('votes', 'value'),
     Input('genres', 'value'),
     Input('description', 'value')])
def predict(title, year, certification, rating, metascore, usa_box_office, votes, chosen_genres, description):

    def genres_(df):
        """Manual OneHotEncoding of genres"""
        df = df.copy() 
        df[genres] = 0
            
        # Set genre to 1 if contained
        for i, item in zip(df.index, df['Genres']):
            if not item:
                break
            item = str(item).lstrip("[").rstrip("]").replace("'","").split(', ')
            for genre in item:
                df.at[i, genre] = 1
        
        df[genres] = df[genres].astype(int)
        
        try:
            df.drop(columns=['nan'], inplace=True)
        except KeyError:
            pass

        return df

    def wrangle(df):
        """Basic wrangle. Calls other 'wrangle' functions. Drops unnecessary/unwanted columns. Also feature engineering"""
        df = df.copy()

        df = genres_(df)

        df['Description Length'] = df['Description'].apply(lambda x: len(str(x)) if x else 0)

        try: 
            df['Metascore'] = df['Metascore'].astype(int)
        except TypeError:
            pass
        except ValueError:
            pass

        try: 
            df['USA Box Office'] = df['USA Box Office'].astype(int)
        except TypeError:
            pass
        except ValueError:
            pass

        df = df.drop(columns=['Genres', 'Description', 'Title'])

        return df

    data = {title:{
        'Title': title,
        'Year': year,
        'Certification': certification, 
        'Rating': rating, 
        'Metascore': metascore, 
        'USA Box Office': usa_box_office, 
        'Votes': votes,
        'Genres': chosen_genres,
        'Description': description,
    }}

    df = pd.DataFrame(
       data
    ).T
    df.fillna(value=np.NaN, inplace=True)
    df = wrangle(df)

    df = df[['Year', 'Certification', 'Rating', 'Metascore', 'Votes',
       'USA Box Office', 'Mystery', 'War', 'Sci-Fi', 'Animation', 'Western',
       'Biography', 'Action', 'Thriller', 'Comedy', 'Music', 'Romance',
       'Musical', 'Family', 'Crime', 'Sport', 'Adventure', 'Film-Noir',
       'Fantasy', 'Drama', 'Horror', 'History', 'Description Length']]


    pipeline = load('model/ridge.joblib')
    y_pred = pipeline.predict(df)[0]

    # return f'Predicted Runtime: {y_pred_log:.2f}%'
    return f'Predicted Runtime: {y_pred:.0f}'
