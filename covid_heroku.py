# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 22:13:10 2020

@author: ABCD
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df_death=pd.read_csv("time_series_19-covid-Deaths.csv")
df_rec=pd.read_csv("time_series_19-covid-Recovered.csv")
df_conf=pd.read_csv("time_series_19-covid-Confirmed.csv")

def stats_calculator(df_conf,df_death,df_rec):
    """
    Docstring:
    Calculate the number of Total Deaths, Confirmed Cases, Recoveries, New Cases and Mortality Rate each day
    
    Takes in confirmed, death and recovered dataframes as argument
    Return a dataframe
    """
    #Extract dates
    date=df_death.keys()[4:]
    
    #Initialize Stats
    total_death_date=[]
    total_rec_date=[]
    total_conf_date=[]
    mortality_rate=[]
    
    #Append Stats
    for i in date:
        total_death_date.append(df_death[i].sum())
        total_rec_date.append(df_rec[i].sum())
        total_conf_date.append(df_conf[i].sum())
        mortality_rate.append(df_death[i].sum()*100/df_conf[i].sum())

    #Make stats into a dataframe
    df_temp_dict={"Date":date, "Death":total_death_date,"Rec":total_rec_date,
                  "Conf":total_conf_date,"MortRate":mortality_rate}
    df_temp=pd.DataFrame(df_temp_dict)
    df_temp['NewConf']=df_temp.Conf
    for i in range(1,df_temp.shape[0]):
        df_temp.NewConf[i]=df_temp.Conf[i]-df_temp.Conf[i-1]
    
    #Return dataframe
    return(df_temp)
    
    
def stats_plotter(df_temp):
    """
    Docstring: 
    Input dataframe object
    Plots Total Confirmed Cases, Recovered Cases, Total Deaths Vs Date 
    """
    
    #Print Latest Stats
    st.markdown(f"Total Confirmed Cases : {df_temp.Conf.iloc[-1]}")
    st.markdown(f"Total Recovered Patients : {df_temp.Rec.iloc[-1]}")
    st.markdown(f"Total Deaths : {df_temp.Death.iloc[-1]}")
    
    #Plot Stats
    sns.set(style="dark")
    plt.figure(figsize=(12,6))
    plt.title("COVID-19 Time Series")
    plt.plot(df_temp.Date,df_temp.Death, label="Death")
    plt.plot(df_temp.Date,df_temp.Conf, label="Confirmed Cases")
    plt.plot(df_temp.Date,df_temp.Rec, label="Recovered")
    plt.xticks(rotation=90)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    st.pyplot()
    
    #Plot Mortality Rate
    st.markdown("*Mortality Rate: "+ str(round(df_temp.MortRate.iloc[-1],2))+"%")
    plt.figure(figsize=(12,4))
    plt.title("COVID-19 Mortality Rate (in %) Vs Time")
    plt.plot(df_temp.Date,df_temp.MortRate, label="Mortality Rate")
    plt.xticks(rotation=90)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    st.pyplot()
    
def only_country(country_name):
    """
    Input- Country Name
    Output- Data of that country
    """
    df_death_ctry=df_death[df_death["Country/Region"]==country_name]
    df_rec_ctry=df_rec[df_rec["Country/Region"]==country_name]
    df_conf_ctry=df_conf[df_conf["Country/Region"]==country_name]

    return(stats_calculator(df_conf_ctry,df_death_ctry,df_rec_ctry))

def except_country(country_name):
    """
    Input- Country Name
    Output- Data outside that country
    """
    df_death_ctry=df_death[df_death["Country/Region"]!=country_name]
    df_rec_ctry=df_rec[df_rec["Country/Region"]!=country_name]
    df_conf_ctry=df_conf[df_conf["Country/Region"]!=country_name]

    return(stats_calculator(df_conf_ctry,df_death_ctry,df_rec_ctry))

#Global Situation    
    
st.title("COVID-19: TIME SERIES")
df_all=except_country("")
st.header(f"Global Situation as on {df_all.Date[df_all.shape[0]-1]}")
stats_plotter(df_all)

st.title("Country wise Time Series")
#selectbox
r_name=df_death["Country/Region"].unique()
re_sel_name=st.selectbox("Select Country", (r_name))
stats_plotter(only_country(re_sel_name))

st.markdown("\n\n\n\* Mortality Rate is calculated as (total deaths recorded/total confirmed cases)*100")
st.markdown("\n\n\nSource: Johns Hopkins CSSE")