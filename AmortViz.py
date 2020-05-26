
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go  
import numpy as np


app = dash.Dash()


#create graph for default values 
payNumber = list(np.linspace(1,360, 360))
intPayments = []
princPayments = []
defaultPrice = 100000
defaultRate = 0.02
r = defaultRate/100/12
defaultPayment = defaultPrice*((r*((1+r)**360))/((1+r)**360-1))
    
for payment in payNumber:
    thisInt = np.ipmt(defaultRate/12, payment , 360, defaultPrice)*-1
    intPayments.append(thisInt)
    princPayments.append(defaultPayment-thisInt)


trace1 = go.Bar(x=payNumber, y=princPayments, name='principal')
trace2 = go.Bar(x=payNumber, y=intPayments, name='interest')
data=[trace1, trace2]
layout = go.Layout(title='Payment Schedule', barmode='stack', 
    xaxis={'title':'Payment Number'}, 
    yaxis={'title':'Payment Amount'})
fig = go.Figure(data=data, layout=layout)




app = dash.Dash(__name__)
app.layout = html.Div([
    html.H3('Price'), 
    html.Div(
    dcc.Slider(
        id='price-slider',
        min=50000,
        max=2000000,
        step=500,
        value=100000
    )),html.H3('Rate'), 
    html.Div(
    dcc.Slider(
        id='rate-slider',
        min=0.01,
        max=0.08,
        step=0.005,
        value=0.02
    )),

    html.Div(id='slider-output-container',style={'font-size':18, 
    'padding': '30px', 
    'border': '4px solid black'
    }),
html.Div(
    dcc.Graph(figure=fig, id='myGraph')
 ) ], style={'width':'75%'})

#link rate and price to output monthly payment amount 
@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('rate-slider', 'value'),
    dash.dependencies.Input('price-slider', 'value')])


def output_payment(rate, price):
    r = rate/12
    pymt = price*((r*((1+r)**360))/((1+r)**360-1))
    pymt= round(pymt,2)

    return 'Your price {:,}'.format(price), " rate is {}".format(rate), " payment is {:,}".format(pymt)



#link rate and price to dynamically update graph
@app.callback(
    dash.dependencies.Output('myGraph', 'figure'), 
    [dash.dependencies.Input('rate-slider', 'value'), 
    dash.dependencies.Input('price-slider', 'value')]
)

def update_graph(rate, price):
    r = rate/12
    pymt = price*((r*((1+r)**360))/((1+r)**360-1))
    pymt= round(pymt,2)

    payNumber = list(np.linspace(1,360, 360))
    intPayments = []
    princPayments = []

    for period in payNumber:
        thisInt = np.ipmt(rate/12, period , 360, price)*-1
        thisInt = round(thisInt,2)
        intPayments.append(thisInt)
        princPayments.append(pymt-thisInt)



    trace1 = go.Bar(x=payNumber, y=princPayments, name='principal')
    trace2 = go.Bar(x=payNumber, y=intPayments, name='interest')
    data=[trace1, trace2]
    layout = go.Layout(title='Payment Schedule', barmode='stack', 
    xaxis ={'title':'Payment Number'}, 
    yaxis={'title':'Payment Amount'})
    fig = go.Figure(data=data, layout=layout)
    return fig




app.run_server(use_reloader=False)