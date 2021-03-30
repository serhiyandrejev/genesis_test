# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 14:18:09 2021

@author: Chaev-Tech
"""
import numpy as np 
import pandas as pd
import plotly.express as px



colors = ['#ffc04d', '#ffae1a', '#ffb733', '#ffa500',
           '#ffc04d', '#b37400', '#cc8400', '#e69500',
           "#ffd000", "#ffba00", "#ffa500"]

def preprocess(df):
  bins = [0,4,8,12,16,20,24]
  time_list = ['Late Night', 'Early Morning','Morning','Noon','Eve','Night']
  df['ARPU'] = 0
  country_list = ['USA', 'CAN', 'AUS', 'GBR']

  df["install_time"] = pd.to_datetime(df['install_time'])
  df.loc[((df.countrycode.isin(country_list)) & (df['os'] == 'ios')), 'ARPU'] = 0.05
  df.loc[((df.countrycode.isin(country_list)) & (df['os'] == 'android')), 'ARPU'] = 0.03
  df.loc[((~df.countrycode.isin(country_list)) & (df['os'] == 'ios')), 'ARPU'] = 0.03
  df.loc[((~df.countrycode.isin(country_list)) & (df['os'] == 'android')), 'ARPU'] = 0.02
  df['hour'] = df['install_time'].dt.hour
  df['time_of_day'] = pd.cut(df['hour'], bins=bins, labels=time_list, include_lowest=True)
  return df

def describe_by_time(df):
  _df = df.groupby(['time_of_day']).count()
  _df1 = df.groupby(['time_of_day']).sum()
  return _df['Unnamed: 0'].index , _df['Unnamed: 0'].values, _df1['ARPU'].index, _df1['ARPU'].values

def describe_by_ARPU(df, by="countrycode"):
  _df = df.groupby([by]).sum()
  _df.sort_values(by=['ARPU'], ascending=False)
  return _df['ARPU']

def describe_set(df, n):
  top_CH = df['channel_id'].value_counts()[:n]
  top_OS = df['os'].value_counts()[:5]
  top_devices = df['device'].value_counts()[:10]
  return top_CH, top_OS, top_devices

def plot_count_ARPU(df, window_type):
  if window_type == "Days":
    df1 = df.resample("D", on="install_time").ARPU.sum()
    df2 = df.resample("D", on="install_time").user_id.count()
  else: 
    df1 = df.resample("W", on="install_time").ARPU.sum()
    df2 = df.resample("W", on="install_time").user_id.count()

  fig_count = px.area(df2, x=df2.index, y=df2.values, title="Installations by:"+window_type,
               color_discrete_sequence=colors)
  fig_count.update_xaxes(title_text=window_type)
  fig_count.update_yaxes(title_text='Installation counts')
  fig_count.update_layout(plot_bgcolor="#fbfbfb")
  fig_count.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#d4d4d4')


  fig_ARPU = px.area(df1, x=df1.index, y=df1.values, title="Income by:"+window_type,
               color_discrete_sequence=colors)
  fig_ARPU.update_xaxes(title_text=window_type)
  fig_ARPU.update_yaxes(title_text='ARPU Sum')
  fig_ARPU.update_layout(plot_bgcolor="#fbfbfb")
  fig_ARPU.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#d4d4d4')

  return fig_count, fig_ARPU