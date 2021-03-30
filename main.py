# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 20:41:42 2021

@author: Chaev-Tech
"""

import streamlit as st
import numpy as np 
import pandas as pd
import plotly.express as px


import utils

colors = ['#ffc04d', '#ffae1a', '#ffb733', '#ffa500',
           '#ffc04d', '#b37400', '#cc8400', '#e69500',
           "#ffd000", "#ffba00", "#ffa500"]

#url = 'https://storage.googleapis.com/nebula-main/data_for_dashboard.csv'
#urllib.request.urlretrieve(url, 'data.csv')
#try: 
 #   df = pd.read_csv('C:/Users/Chaev-Tech/ml_kit/preprocessed.csv')
 #   print('preprocessed_data is loaded')
#except:    
df = pd.read_csv('data_dash.csv')
print('preprocessing the data')
df["install_time"] = pd.to_datetime(df['install_time'])

st.sidebar.title("Test Task 2")
st.sidebar.header("Choose dates")
date_st = st.sidebar.date_input("Left date",
                                min_value=df['install_time'].min().date(),
                                max_value=df['install_time'].max().date(),
                                value=df['install_time'].min().date())
st.sidebar.text("By default the left date is: " +
                str(df['install_time'].min().date()))
date_fin = st.sidebar.date_input("Right date",
                                min_value=date_st,
                                max_value=df['install_time'].max().date(),
                                value=df['install_time'].max().date()) 
st.sidebar.text("By default the reight date is:" + 
                str(df['install_time'].max().date()))

df = df[(df['install_time'].dt.date >= date_st) & (df['install_time'].dt.date <= date_fin)]



st.header("Installation and APRU sum")
window_type = st.selectbox("Select time period", ("Days", "Weeks"))
fig_count, fig_ARPU = utils.plot_count_ARPU(df, window_type)
st.plotly_chart(fig_count, False)
st.plotly_chart(fig_ARPU, False)

_1 = utils.describe_by_ARPU(df)
_2 = utils.describe_by_ARPU(df, by='channel_id')


col1,col2 = st.beta_columns([1,1])
col1.subheader("Top Country by ARPU sum")
col1.table(_1.sort_values(ascending=False)[:10])
col2.subheader("Top Channels by ARPU sum")
col2.table(_2.sort_values(ascending=False)[:10])

col1 , col2 = st.beta_columns([2,1])
col1.header("Country analysis")
if col1.checkbox("Select certain country"):
    options=col1.multiselect("What country you want to look?", options=df['countrycode'].unique())
    df = df[df['countrycode'].isin(options)]
n = col1.slider("Select num of top-rows", min_value=5, max_value=20)

top_CH, top_OS, top_devices = utils.describe_set(df, n)
col1.subheader("Top of devices by overall/countrycode")

col1.table(top_devices)
col2.subheader("Top of channels by overall/countrycode")
col2.table(top_CH)
col2.subheader("Top of OS by overall/countrycode")
col2.table(top_OS)




fig = px.pie(values=top_CH.values, names=top_CH.index, title='Top channels',
             color_discrete_sequence=colors)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig,True)


col1 , col2 = st.beta_columns([15,15])
fig = px.pie(values=top_OS.values, names=top_OS.index, title='Top OS',
             color_discrete_sequence=colors)
fig.update_traces(textposition='inside', textinfo='percent+label')
col1.plotly_chart(fig,True)
fig = px.pie(values=top_devices.values, names=top_devices.index, title='Top devices',
             color_discrete_sequence=colors)
fig.update_traces(textposition='inside', textinfo='percent+label')
col2.plotly_chart(fig, True)

st.header("Time of day analysis")
_cindex, _cvalues, _sindex, _svalue = utils.describe_by_time(df)

fig = px.area(x=_cindex, y=_cvalues, title="Count of installation by time of day",
              color_discrete_sequence=colors)
fig.update_xaxes(title_text="Time of day")
fig.update_yaxes(title_text='Installation counts')
fig.update_layout(plot_bgcolor="#fbfbfb")
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#d4d4d4')
st.plotly_chart(fig)
fig = px.area(x=_sindex, y=_svalue, title="Sum of ARPU by time of day",
              color_discrete_sequence=colors)
fig.update_xaxes(title_text="Time of day")
fig.update_yaxes(title_text='ARPU sum')
fig.update_layout(plot_bgcolor="#fbfbfb")
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#d4d4d4')
st.plotly_chart(fig)