from dash.dependencies import Input, Output, State
import dash_core_components as dcc
from dash_core_components.Markdown import Markdown
from dash_core_components.Textarea import Textarea
import dash_html_components as html
from dash_html_components.Mark import Mark

from joblib import load
import numpy as np
import pandas as pd

from app import app
from find_title import get_titles, get_title_info

genres = ['Action',
 'Adventure',
 'Animation',
 'Biography',
 'Comedy',
 'Crime',
 'Drama',
 'Family',
 'Fantasy',
 'Film-Noir',
 'History',
 'Horror',
 'Music',
 'Musical',
 'Mystery',
 'Romance',
 'Sci-Fi',
 'Sport',
 'Thriller',
 'War',
 'Western']

certifications = ['R', 'PG-13', 'Approved', 'PG', 'Not Rated', 'G', 'Passed', 'TV-14', 'GP', 'TV-PG', 'TV-MA', 'Unrated', 'NC-17', 'M']

style = {'padding': '.5em', 'paddingLeft': '1.5em', 'margin': '.1em'}

titles = {None: None}

layout = html.Div([
    dcc.Markdown("""
    &nbsp

    Enter information about a movie. [IMDb](https://www.imdb.com/) is your best place for information.
    """),
    html.Div(id='prediction-content', style={'marginBottom': '0em', **style, 'fontSize':20}), 

    html.Div([
        dcc.Markdown('###### Title'), 
        dcc.Input(
            id='title',
            type='text',
            value='',
            debounce=True
        ),
        html.Button('Search', id='search')
    ], style=style), 

    html.Div([
        dcc.Markdown('Top matching titles:'),
        dcc.Markdown(children=f'{titles.items()}', 
                     id='top-title'),
        html.Button('Autofill Match', id='autofill'),
        dcc.Markdown('Gathers data it can from IMDb.com. Might not get all info required.')
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
    ], style=style),

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
            marks={n: str(n)[:-6]+'M' for n in range(0,1000000001,50000000)}
        )
    ], style=style),

    html.Div([
        dcc.Markdown('###### Number of Votes'), 
        dcc.Slider(
            id='votes', 
            min=0, 
            max=1500000, 
            step=1000, 
            #value=1500000, 
            marks={n: str(n)[:-3]+'K' for n in range(0,1500001,100000)}
        )
    ], style=style),

    html.Div([
        dcc.Markdown('###### Genres'), 
        dcc.Dropdown(
            id='genres', 
            options=[{'label': genre, 'value': genre} for genre in genres], 
            multi=True
        ), 
    ], style=style),

    html.Div([
        dcc.Markdown('###### Movie Description'),
        dcc.Textarea(
            id='description',
            style={'width': '100%'}
        )
    ], style=style),

    html.Button('Predict', id='predict'),


], style={**style, 'textAlign': 'center'})

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

    global titles
    titles = get_titles(title)

    df = pd.DataFrame(
       data
    ).T
    df.fillna(value=np.NaN, inplace=True)
    df = wrangle(df)

    df = df[['Year', 'Certification', 'Rating', 'Metascore', 'Votes', 'USA Box Office', 'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western', 'Description Length']]


    pipeline = load('model/ridge.joblib')
    y_pred = pipeline.predict(df)[0]

    # return f'Predicted Runtime: {y_pred_log:.2f}%'
    return f'Predicted Runtime: {max(0, y_pred):.2f} minutes'


@app.callback(
    Output('top-title', 'children'),
    [Input('search', 'n_clicks')],
    [State('title', 'value')],)
def search(n_clicks, value):
    x = 1
    titles = get_titles(value)
    if titles:
        return '&nbsp  \n\n'.join(list(titles.keys())[:x])
    return ''


@app.callback([
    Output('year', 'value'),
    Output('certification', 'value'),
    Output('rating', 'value'),
    Output('metascore', 'value'),
    Output('usa_box_office', 'value'),
    Output('votes', 'value'),
    Output('genres', 'value'),
    Output('description', 'value')], # Title Input text
    [Input('autofill', 'n_clicks')], # Button click
    [State('title', 'value')],)
def autofill(n_clicks, value):
    print('button clicked')
    title = get_titles(value, True)
    if title:
        title = list(title.values())[0]
    else:
        return [None] * 8
    return get_title_info(title)

