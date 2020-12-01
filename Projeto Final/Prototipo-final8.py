import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go 
import json
from dash.dependencies import Input, Output

# Dados do mapa
brazil_states = json.load(open("brazil-states.geojson",'r'))

# Dados Gráfico de linha
cols = ['Anos','state_names','Consumo']
df_dados = pd.read_csv("dados-8.csv",usecols=cols,low_memory=False)

#A função unique() retorna uma lista com todas as categorias constantes em uma coluna.

states_names=df_dados['state_names'].unique()

app = dash.Dash(__name__)

#Dados do Gráfico de pizza
df1 = pd.read_csv('dados_pizza.csv')

#Primeiro Gráfico do Dashboard- Consumo Médio de Energia Elétrica 1995 - 2019

trace1 = go.Bar(x = ['1995', '1996', '1997', "1998", "1999", "2000" , "2001" ,"2002","2003","2004","2005","2006","2007",
"2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019"],
y = [243074,257330,273280,284522,292188,307592,283257,293226,306987,331865,345336,356129,377030,388472,384306,415668,433016,448126,463142,474823,
465987,462068,467475,475237,482083])
data1 = [trace1]
layout1 = go.Layout(title = "",
                   yaxis={'title': 'Consumo (GWh)'},
                   xaxis ={'title': 'Anos'})
fig1 = go.Figure(data=data1,layout=layout1)

# Gráfico de mapa do Brasil-2019

state_id_map = {}
for feature in brazil_states["features"]:
    feature ["id"] = feature["properties"] ["id"]
    state_id_map [feature["properties"] ["sigla"]] = feature["id"]


df = pd.read_excel ("mapa-brazil-test3.xlsx")
df['Consume']= df['Consume'].apply(lambda x: int((x.split("/")[0].replace(",", ""))))
df['id'] = df['STATE'].apply (lambda x: state_id_map[x] )
df.head()

fig2 = px.choropleth(
    df,
    locations="id",
    geojson=brazil_states,
    color="Consume",
    hover_name="STATE",
    hover_data=["Consume"],
    title="",
)
fig2.update_geos(fitbounds="locations", visible=False)

#Gráfico de tipo de fonte

trace3 = go.Bar(x = ['Gás Natural','Carvão Natural','Lenha','Bagaço de cana','Lixívia','Outras Recuperações','Biodisel','Gàs de Coqueira','Coque de carvão mineral','Eletricidade','Carvão Vegetal','Alcool Etílico','Alcatrão','Derivados de petroleo','Óleo diesel','Óleo combustivel','Gasolina','Gás liquifeito de petroleo','Querosene','Outas secundarias de petroleo'
],
y = [221703,45055,194896,320162,80456,13526,48544,16829,90435,535503,42356,182893,1058330,1021172,497113,28656,251150,95238,39437,109601
])
data3 = [trace3]
layout3 = go.Layout(title = "",
                   yaxis={'title': 'Consumo (KWh)'},
                   xaxis ={'title': 'Tipos de fonte'})



fig3 = go.Figure(data=data3,layout=layout3)


# Grafico de Fontes Renováveis

fig4 = go.Figure()

fig4.add_trace(
    go.Pie(labels=['Derivados da Cana-de-açúcar', 'Hidráulica', 'Lenha e Carvão Vegetal','Eólica', 'Solar','Outras Renováveis'],
               values=[6145408,4229133,3027754,5599854,665236,1781135],
               name="Oferta Interna de Energia Renovável (10⁶ KWh)",
               ))
fig4.add_trace(
    go.Pie(labels=['Urânio', 'Carvão Mineral e Coque', 'Gás Natural', 'Petróleo e Derivados','Outras Não Renováveis'],
               values=[48.54362,180.0324,417.6217,1175.223,20.7014],
               name="Oferta Interna de Energia Não Renovável (10⁶ kWh)",
               ))

# Menu do Grafico de Fontes Renovaveis

fig4.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Renovavel",
                     method="update",
                     args=[{"visible": [True, False]},
                           {"title": ""}]),
                dict(label="Não renovavel",
                     method="update",
                     args=[{"visible": [False, True]},
                           {"title": ""}])

     

    
            ]),
    )])
fig4.update_layout(title_text="")

#Grafico de consumo por setor

fig5 = go.Figure()

fig5.add_trace(
    go.Pie(labels=df1['labels'],
               values=df1['Brasil'],
               name="Brasil",
               ))
fig5.add_trace(
    go.Pie(labels=df1['labels'],
               values=df1['Norte'],
               name="Norte",
               ))
fig5.add_trace(
    go.Pie(labels=df1['labels'],
               values=df1['Nordeste'],
               name="Nordeste",
               ))
fig5.add_trace(
    go.Pie(labels=df1['labels'],
               values=df1['Sudeste'],
               name="Sudeste",
               ))
fig5.add_trace(
    go.Pie(labels=df1['labels'],
               values=df1['Sul'],
               name="Sul",
               ))
fig5.add_trace(
    go.Pie(labels=df1['labels'],
               values=df1['Centro Oeste'],
               name="Centro Oeste",
               ))           

# Menu do Gráfico de Setor 

fig5.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Brasil",
                     method="update",
                     args=[{"visible": [True, False, False, False, False, False,]},
                           {"title": "Brasil"}]),
                dict(label="Norte",
                     method="update",
                     args=[{"visible": [False, True, False, False, False, False,]},
                           {"title": "Norte"}]),
                dict(label="Nordeste",
                     method="update",
                     args=[{"visible": [False, False, True, False, False, False,]},
                           {"title": "Nordeste"}]),
                dict(label="Sudeste",
                     method="update",
                     args=[{"visible": [False, False, False, True, False, False,]},
                           {"title": "Sudeste"}]),
                dict(label="Sul",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, False,]},
                           {"title": "Sul"}]),
                dict(label="Centro Oeste",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, True,]},
                           {"title": "Centro Oeste"}])
     

    
            ]),
    )])
fig5.update_layout(title_text="")


#Callback do Graficco de linha

@app.callback(
   Output('line-result','figure'),
   [Input('state-dropdown','value')])

def update_output(value):
        df_filtered = df_dados[df_dados.state_names == value].groupby("Anos").sum().reset_index()
        return px.line(df_filtered,x=cols[0],y=cols[2])

# Estilo do dashboard

app.layout = html.Div(children=[
    html.H1(children='Dashboard - Matriz Energética'),

    html.Div(children='''
        Matriz Energetica/Eletrica brasileira
    '''),


#Titulo do Primeiro Gráfico

    html.Div(id="title-graf4", children=[
        html.H1(children='Consumo Médio de Energia Elétrica 1995 - 2019')
    ], style={
        'text-align': 'center'
    }),

#Grafico do primeiro grafico

     dcc.Graph(
        figure=fig1, 
    ),
    
#Titulo do Grafico de mapa

    html.Div(id="title-graf2", children=[
        html.H1(children='Consumo de Energia Elétrica no Brasil')
    ], style={
        'margin-left': '55%',
        'width': '40%',
        "position":'absolute',
        'z-index':'10',

    }),

    #gráfico de mapa do Brasil

    dcc.Graph(
        figure=fig2,style={
        'width': '50%',
        'height': '45%',
        'float': 'right',
        'padding': '20px',
        'margin-top':'5%'}),
    
 # Título do Grafico de linha

    html.Div(id="graph-5", children=[
        html.H1(children='Consumo de Energia Elétrica por UF em Gwh ')
    ], style={
        'width':'55%',
            }),
   
# Menu do Gráfico de linha
    
    dcc.Dropdown(
       id='state-dropdown',
       value = "Brasil",
       options=[{'label':i,'value':i} for i in states_names],
       style={'width': '55%',
        'height': '10%',
        'padding': '5px',
        'margin-left': '1cm'}

#Grafico de Linha

   ),
   html.Div([
       dcc.Graph(
           id='line-result',style={
        'width': '55%',
        'height': '50%',
        'padding': '20px'}
       )
   ]),
    
# titulo do grfico de fonte utiizado

    html.Div(id="title", children=[
        html.H1(children='Tipo de Fonte Utilizado')
    ], style={
        'text-align': 'center',
        'width': '40%',
        'margin-left': "30%"

#Grafico de fonte utlizado  
  
    }),
    dcc.Graph(
        figure=fig3
    ),
    
 
    #Titulo de Gráfico por Setor
    html.H1(
        'Consumo médio de energia por setor',
        style={
            'position':'absolute',
            'z-index': "10"
            }

    #Titulo do grafico de fontes renovaveis e nao-renovaveis

    ),
    html.H1(
        "Fontes renováveis e não-renováveis",
        style={
            'position':'absolute',
            'z-index': '10',
            'margin-left': "55%" ,

        }
#Grafico de Fontes renováveis e não-renováveis
    ),
    dcc.Graph(
        figure=fig4,style={
        'width': '45%',
        'height': '40%',
        'float': 'right',
        'padding': '20px',
        'margin-left': '55%',
       

        }), 

    
#Gráfico de Setor
    dcc.Graph(
        figure=fig5,style={
        'width': '50%',
        'height': '50%',
        'padding': '20px'}),
        

        
    
])

if __name__ == '__main__':
    app.run_server(debug=True)
    