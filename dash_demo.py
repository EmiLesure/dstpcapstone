#Draft of script to create dashboards in Dash
#started June 13, 2025, last edit June 17, 2025
# uses weights


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, Input, Output, dcc, html, dash_table

df = pd.read_csv("df_inter_state.csv")


####################################################################
################ Variable Recode Section ###########################


# Recode education variable
def edugroups(series): 
    if series in ['No schooling', 'Elementary/Middle school', 'Some high school']:
        return 'Less than high school'
    elif series =='High school graduate':
        return 'High school graduate'
    elif series in ['Some college', "Associate's degree"]:
        return 'Some college'
    elif series == "Bachelor's degree":
        return "Bachelor's degree"
    elif series == 'Graduate degree':
        return 'Graduate degree'
    else:
        return 'Other' 

df['education2']=df['education'].apply(edugroups)

# Recode age variable
def agegroup (series):
    if series <18:
        return '0-17 years'
    elif 18<= series < 25:
        return '18-25 years'
    elif 25 <= series < 35:
        return '25-34 years'
    elif 35 <= series < 45:
        return '35-44 years'
    elif 45 <= series < 55:
        return '45-54 years'
    elif 55 <= series < 65:
        return '55-64 years'
    elif 65 <= series: 
        return "65+ years"
    else: 
        return 'Other'
        
df['age2']=df['age'].apply(agegroup)

# Recode marital status variable
def maritalgroup (series):
    if series in ['Divorced', 'Separated']:
        return "Divorced/Separated"
    elif series == 'Married':
        return 'Married'
    elif series == 'Never Married':
        return 'Never Married'
    elif series == 'Widowed':
        return 'Widowed'
    else:
        return 'Other' 

df['marital_status2']=df['marital_status'].apply(maritalgroup)

# Recode current_state using two letter abbreviation

# tranform states into two letter state abbreviations
# code from https://medium.com/@jason_the_data_scientist/python-mapping-state-abbreviations-to-state-and-vice-versa-in-pandas-e4cd24edefb0

#Define function
def state_abbrev_mapping(df, col, output_abbr = False, add_new_col = False, new_col = None,  case = None):
    #df =  the Pandas dataframe.
    #col = String. The column with the state name or abbreviation you wish to use
    #output_abbr = True/False. Do you want to the output to the the state abbreviation? The other option is the state full name.
    #add_new_col = True/False. Do you want to add a new column? The new column will overwrite the inputted column if not.
    #new_col = String. Name of new column you wish to add.
    #case = 'upper', 'lower', or None. Do you want to specify a letter-case for the data?
 
#List of states
    state2abbrev = {
        'Alaska': 'AK',
        'Alabama': 'AL',
        'Arkansas': 'AR',
        'Arizona': 'AZ',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'District of Columbia': 'DC',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Iowa': 'IA',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Massachusetts': 'MA',
        'Maryland': 'MD',
        'Maine': 'ME',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Missouri': 'MO',
        'Mississippi': 'MS',
        'Montana': 'MT',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Nebraska': 'NE',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'Nevada': 'NV',
        'New York': 'NY',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Virginia': 'VA',
        'Vermont': 'VT',
        'Washington': 'WA',
        'Wisconsin': 'WI',
        'West Virginia': 'WV',
        'Wyoming': 'WY',
        'Puerto Rico': 'PR',
        'Virigin Islands': 'VI'
    }
 
    #List of states
    abbrev2state = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming',
        'PR': 'Puerto Rico',
        'VI': 'Virigin Islands'
    }
     
    #If user wants to add a new column
    if add_new_col == False:
         
        #Is the output an abbreviation?
        if output_abbr == True:
            df[col] = df[col].str.strip().replace(state2abbrev)
        else:
            df[col] = df[col].str.strip().replace(abbrev2state)
             
        #Does the user want a specific case sensitivity?
        if case == 'upper':
            df[col] = df[col].str.upper()
        elif case == 'lower':
            df[col] = df[col].str.lower()
             
    #If user not want to add a new column       
    if add_new_col == True:
         
        #If new column name is missing
        if new_col == None:
            #Prompt user to enter a new column name
            print("Error: You requested to add a new column but did not specify a new column name. Please add a column name with new_col = ''")
            return()
         
        #Is the output an abbreviation?
        if output_abbr == True:
            df[new_col] = df[col].str.strip().replace(state2abbrev)
        else:
            df[new_col] = df[col].str.strip().replace(abbrev2state)
 
        #Does the user want a specific case sensitivity?
        if case == 'upper':
            df[new_col] = df[new_col].str.upper()
        elif case == 'lower':
            df[new_col] = df[new_col].str.lower()
 
    return(df)
 
 
#Call Function 
state_abbrev_mapping(df = df,
                     col= 'current_state',
                     output_abbr = True,
                     add_new_col = True,
                     new_col = 'current_state2',
                     case = 'upper')

state_abbrev_mapping(df = df,
                     col= 'previous_state',
                     output_abbr = True,
                     add_new_col = True,
                     new_col = 'previous_state2',
                     case = 'upper')


####################################################################
################ Dash Layout and Dropdowns #########################

# Style settings
external_stylesheets = [
    {"href": ("https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",},
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Layout
app.layout = html.Div([
    html.H1("Weighted Counts of Movers by Previous and Current State of Residence"),

    html.Div([
        html.Label('Select Sex:'),
        dcc.Dropdown(
            id='sex-dropdown',
            options=[{'label': sex, 'value': sex} for sex in df['sex'].dropna().unique()],
            value=['Female'],
            multi=True
        )
    ], style={'width': '20%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Select Age:'),
        dcc.Dropdown(
            id='age-dropdown',
            options=[
                {'label': '0-17 years', 'value': '0-17 years'}, 
                {'label': '18-25 years', 'value': '18-25 years'}, 
                {'label': '25-34 years', 'value': '25-34 years'},
                {'label': '35-44 years', 'value': '35-44 years'},
                {'label': '45-54 years', 'value': '45-54 years'},
                {'label': '55-64 years', 'value': '55-64 years'},
                {'label': '65+ years', 'value': '65+ years'}
            ],
            value=['0-17 years'],
            multi=True
        )
    ], style={'width': '20%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Select Highest Level of Education:'),
        dcc.Dropdown(
            id='edu-dropdown',
            options=[
                {'label': 'Less than High School', 'value': 'Less than high school'},
                {'label': 'High School Graduate', 'value': 'High school graduate'},
                {'label': 'Some College', 'value': 'Some college'},
                {'label': "Bachelor's Degree", 'value': "Bachelor's degree"},
                {'label': 'Graduate Degree', 'value': 'Graduate degree'}
            ],
            value=['Less than high school'],
            multi=True
        )
    ], style={'width': '20%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Select Marital Status:'),
        dcc.Dropdown(
            id='marital-dropdown',
            options=[{'label': status, 'value': status} for status in df['marital_status'].dropna().unique()],
            value=[df['marital_status'].dropna().unique()[0]],
            multi=True
        )
    ], style={'width': '20%', 'display': 'inline-block'}),

    html.Br(),
    
    html.Div([
        html.Div([
            dcc.Graph(id='map_previous', style={'display': 'inline-block'}), 
            dcc.Graph(id='map_current', style={'display': 'inline-block'}),
        ]),
        html.Br(),
        html.Div([
            dcc.Graph(id='bar-chart-previous', style={'display': 'inline-block'}),
            dcc.Graph(id='bar-chart-current', style={'display': 'inline-block'}),
        ])
    ]),
    html.Br(),
    html.Div([
        html.Div([
            dash_table.DataTable(
                id='table_previous',
                columns=[
                    {"name": "Previous State", "id": "previous_state"},
                    {"name": "Weighted Count", "id": "weighted_counts", "type": "numeric"},
                    {"name": "Percentage of Total", "id": "percentage", "type": "numeric", "format": {'specifier': '.1f'}}
                ],
                data=[],
                sort_action="native",
                style_header={'fontWeight': 'bold'},
                style_cell={'textAlign': 'left'},
                style_data_conditional=[
                    {'if': {'filter_query': '{previous_state} = "Total"'},
                    'fontWeight': 'bold',
                    'backgroundColor': '#f9f9f9'}
                ]
            )
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '5%', 'marginLeft': '5%'}),
        
        html.Div([
            dash_table.DataTable(
                id='table_current',
                columns=[
                    {"name": "Current State", "id": "current_state"},
                    {"name": "Weighted Count", "id": "weighted_counts", "type": "numeric"},
                    {"name": "Percentage of Total", "id": "percentage", "type": "numeric", "format": {'specifier': '.1f'}}
                ],
                data=[],
                sort_action="native",
                style_header={'fontWeight': 'bold'},
                style_cell={'textAlign': 'left', 'margin-left': 'auto'},
                style_data_conditional=[
                    {'if': {'filter_query': '{current_state} = "Total"'},
                        'fontWeight': 'bold',
                        'backgroundColor': '#f9f9f9'}
                ]
            )
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '5%', 'marginLeft': '12%'})
    ])
])


# Callback section
@app.callback(
    Output('map_previous', 'figure'),
    Output('map_current', 'figure'),
    Output('bar-chart-previous', 'figure'),
    Output('bar-chart-current', 'figure'),
    Output('table_previous', 'data'),
    Output('table_current', 'data'),
    Input('sex-dropdown', 'value'),
    Input('age-dropdown', 'value'),
    Input('edu-dropdown', 'value'),
    Input('marital-dropdown', 'value')
)

def update_dashboard(selected_sex, selected_age, selected_edu, selected_marital_status):
    if not selected_sex or not selected_age or not selected_edu or not selected_marital_status:
        empty_fig = px.bar(title="Please select at least one option in each dropdown.")
        return empty_fig, empty_fig, empty_fig, empty_fig, [], []
        
    filtered_df = df[
        df['sex'].isin(selected_sex) & 
        df['age2'].isin(selected_age) &
        df['education2'].isin(selected_edu) &
        df['marital_status2'].isin(selected_marital_status)
    ]

    if filtered_df.empty:
        empty_fig = px.bar(title="No data matches the selected filters.")
        return empty_fig, empty_fig, [], []

    # Creation of Bar Chart: Previous State
    
    # Sum weights by previous_state
    wcounts_graph_previous = filtered_df.groupby('previous_state')['person_weight'].sum().reset_index(name='weighted_counts').sort_values(by='weighted_counts', ascending=False)
    # Rename columns
    wcounts_graph_previous.columns = ['previous_state', 'weighted_counts']

     # Set up bar chart for previous state
    fig = px.bar(
        wcounts_graph_previous,
        x='previous_state',
        y='weighted_counts',
        labels={'weighted_counts': 'Weighted Counts', 'previous_state': 'Previous State'},
        #title=f"Count by Previous State for {selected_sex}, {selected_age}, {selected_edu}, {selected_marital_status}"
        )
    fig.update_xaxes(categoryorder='category ascending') # use total descending if sort by value


    # Sum weights by current state
    wcounts_graph_current = filtered_df.groupby('current_state')['person_weight'].sum().reset_index(name='weighted_counts').sort_values(by='weighted_counts', ascending=False)
    wcounts_graph_current.columns = ['current_state', 'weighted_counts']

    # Set up bar chart for current state
    fig2 = px.bar(
        wcounts_graph_current,
        x='current_state',
        y='weighted_counts',
        labels={'weighted_counts': 'Weighted Counts', 'current_state': 'Current State'},
        #title=f"Count by Current State for {selected_sex}, {selected_age}, {selected_edu}, {selected_marital_status}"
        )
    fig2.update_xaxes(categoryorder='category ascending') # use total descending if sort by value

     # Add percentage and total row to weighted counts (for table 1: Previous State)
    total_previous_w = wcounts_graph_previous['weighted_counts'].sum()
    wcounts_table_previous = wcounts_graph_previous.copy()
    wcounts_table_previous['percentage'] = (wcounts_table_previous['weighted_counts'] / total_previous_w * 100).round(1)

    total_row_previous = pd.DataFrame({
        'previous_state': ['Total'],
        'weighted_counts': [total_previous_w],
        'percentage': [100.0]
        })

    wcounts_table_previous2 = pd.concat([wcounts_table_previous, total_row_previous], ignore_index=True)

     # Add percentage and total row (for table 2: Current State)
    total_current_w = wcounts_graph_current['weighted_counts'].sum()
    wcounts_table_current = wcounts_graph_current.copy()
    wcounts_table_current['percentage'] = (wcounts_table_current['weighted_counts'] / total_current_w * 100).round(1)

    total_row_current = pd.DataFrame({
        'current_state': ['Total'],
        'weighted_counts': [total_current_w],
        'percentage': [100.0]
        })

    wcounts_table_current2 = pd.concat([wcounts_table_current, total_row_current], ignore_index=True)

    # create counts for map: Previous State
    wcounts_map_previous=filtered_df.groupby('previous_state2')['person_weight'].sum().reset_index(name='wcount_previous').sort_values(by='wcount_previous', ascending=False)
    wcounts_map_previous.columns = ['previous_state2', 'wcount_previous']

    # create counts for map 2: Current State
    wcounts_map_current=filtered_df.groupby('current_state2')['person_weight'].sum().reset_index(name='wcount_current').sort_values(by='wcount_current', ascending=False)
    wcounts_map_current.columns = ['current_state2', 'wcount_current']
    
     # create map for Previous State
    map_previous = go.Figure(data=go.Choropleth(
        locations=wcounts_map_previous['previous_state2'],
        z = wcounts_map_previous['wcount_previous'].astype(float),
        locationmode='USA-states',
        colorscale = 'Reds',
        colorbar_title = 'Weighted Counts'
     ))
        
    map_previous.update_layout(
        title_text = 'Weighted Counts by Previous State',
        geo_scope = 'usa'
    )
         
     # create map for Current State
    map_current = go.Figure(data=go.Choropleth(
        locations=wcounts_map_current['current_state2'],
        z = wcounts_map_current['wcount_current'].astype(float),
        locationmode='USA-states',
        colorscale = 'Reds',
        colorbar_title = 'Weighted Counts'
     ))
        
    map_current.update_layout(
        title_text = 'Weighted Counts by Current State',
        geo_scope = 'usa'
    )
    
    return map_previous, map_current, fig, fig2, wcounts_table_previous2.to_dict('records'), wcounts_table_current2.to_dict('records')

if __name__ == "__main__":
    app.run_server(jupyter_mode="tab", debug=True, port = 8071)

