import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime

st.title('Covid-19 indonesia cases')
st.write("It shows ***Coronavirus cases*** in Indonesia")
st.sidebar.title("Selector")
#image = Image.open("Coronavirus.jpg")
#st.image(image,use_column_width=True)
st.markdown('<stlye>body{background-color: lightblue;}</style>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("covid_19_indonesia_time_series_all.csv")
    return df
df = load_data()

state = ['Total Cases', 'Total Active Cases', 'Total Deaths']

visualization = st.sidebar.selectbox('Select a chart type',('Bar chart','Pie chart','linechart'))
#state_select = st.sidebar.selectbox('Select a state', df['state'].unique())
state_select = st.sidebar.selectbox('Select a state',state)
status_select = st.sidebar.radio('Covid-19 patient status',("Total Confirmed Cases", "Total Active Cases","Total Death Cases","Total Recovered Cases"))
selected_state = state==state_select
st.markdown("## **State level analysis**")


def get_total_dataframe(df):
    df = pd.read_csv("covid_19_indonesia_time_series_all.csv")
   # date = datetime.strptime(df.loc[df['Date']], '%m/%d/%Y')
    
    total_dataframe = pd.DataFrame({
        #'Status':['Confirmed', 'Recovered','Deaths','Active'],
        #'Number of cases':(df.iloc[0]['Total Cases'], df.iloc[0]['Total Active Cases'], df.iloc[0]['Total Recovered'],df.iloc[0]['Total Deaths']), 
        'Total Cases':(df.iloc[0]['Date'] , df.iloc[0]['Total Cases'])
       
        #'Total Cases':(df.iloc[df['Total Cases']])
    })
    return total_dataframe

state_total = get_total_dataframe(selected_state)

st.line_chart(state_total)


if visualization == 'Bar Chart':
    state_total_graph = px.bar(state_total, x='Status', y='Number of cases', labels={'Number of cases':'Number of cases in %s' % (state_select)}, color = 'Status')
    st.bar_chart(state_total_graph)

elif visualization == 'Pie Chart':
    if status_select== 'Total Confirmed Cases':
        st.title("Total Confirmed Cases ")
        fig = px.pie(df,values=df['Total Cases'], names=df['Total Cases'])
        st.plotly_chart(fig)

    elif status_select=='Total Active Cases':
        st.title("Total Active Cases")
        fig = px.pie(df, values=['Total Active Cases'], names=df['Total Active Cases'])
        st.plotly_chart(fig)

    elif status_select=='Total Deaths Cases':
        st.title("Total Death cases")
        fig = px.pie(df, values=['Total Deaths'], names=df['Total Deaths Cases'])
        st.plotly_chart(fig)

    else: 
        st.title("Total Recovered Cases")
        fig = px.pie(df, values=['Total Recovered'], names=df['Total Recovered Cases'])
        st.plotly_chart(fig)

elif visualization =='Line Chart':
    if status_select == 'Total Deaths cases':
        st.title("Total Death Cases Among states")

def get_table():
    datatable = df[['Date','Location','Total Cases', 'Total Active Cases', 'Total Deaths']].sort_values(by=['Total Cases'],ascending=False)
    return datatable

datatable = get_table()
st.dataframe(datatable)