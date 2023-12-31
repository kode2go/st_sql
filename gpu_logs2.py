import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from datetime import date
import warnings

import streamlit as st
warnings.simplefilter('ignore')
# Go to each GPU node and scan through the information provided in the file
# which contains information for the dates provided above
# The file all should have everything for each node

# Define a function to load data
@st.cache_data
def load_data():
    appended_data = pd.DataFrame()
    # Your data loading and preprocessing code here
    st.write("Getting GPU 200 Data")
    for i in range(1,7):
        j = str(i)
        cols=['date', 'gpunum', 'gpuid', 'hwarenum', 'proc1', 'proc2', 'proc3', 'user', 'code', 'pid']
        df1 = pd.read_csv("logs/gpu/gpu200"+j+"/all", names=cols, header=None, low_memory=False)
        df1['date'] = pd.to_datetime(df1["date"], format="%Y%m%d %H:%M")
        # Count the number of times a specific user appears per day
        df1['day'] = df1['date'].apply(lambda x: "%d-%d-%d" % (x.year,x.month,x.day))
        # Group all codes that are considered MD codes
        df1['code'] = df1.code.str.replace(r'(^.*pmemd.cuda.*$)|(^.*gmx.*$)|(^.*namd2.*$)|(^.*desmond.*$)|(^.*charmm.*$)', 'MD')
        # Group all codes that are considered ML codes
        df1['code'] = df1.code.str.replace(r'(^.*python.*$)|(^.*net3.*$)|(^.*imaging.*$)|(^.*dnls.*$)', 'ML')
        # Group all codes that are considered DEM codes
        df1['code'] = df1.code.str.replace(r'(^.*Rocky.*$)', 'DEM')
        # Group all codes that are considered Cryo-EM codes
        df1['code'] = df1.code.str.replace(r'(^.*relion.*$)', 'RELION')
        # Group everything that is not using the GPU
        df1['code'] = df1.code.str.replace(r'(^.*null.*$)', 'NULL')
        # Everything else
        df1['code'] = df1.code.str.replace(r'(^.*a.out.*$)|(^.*lmp.*$)|(^.*nvidia.*$)|(^.* .*$)', 'OTHER')
        # Count the number of times a specific code appears per day and get percentage
        # Remember that GPU200x nodes have 864 entries per day
        df2 = (df1.groupby(['day', 'code']).size()*100/864).round(1).reset_index(name='percent')
        # Count the number of times a specific code appears per day
        appended_data = pd.concat([appended_data, df2], ignore_index=True)
    
    # Get all GPU400x data and append to same dataframe as above
    st.write("Getting GPU 400 Data")
    for i in range(1,4):
        j = str(i)
        cols=['date', 'gpunum', 'gpuid', 'hwarenum', 'proc1', 'proc2', 'proc3', 'user', 'code', 'pid']
        df1 = pd.read_csv("logs/gpu/gpu400"+j+"/all", names=cols, header=None, low_memory=False)
        df1['date'] = pd.to_datetime(df1["date"], format="%Y%m%d %H:%M")
        # Count the number of times a specific user appears per day
        df1['day'] = df1['date'].apply(lambda x: "%d-%d-%d" % (x.year,x.month,x.day))
        # Group all codes that are considered MD codes
        df1['code'] = df1.code.str.replace(r'(^.*pmemd.cuda.*$)|(^.*gmx.*$)|(^.*namd2.*$)|(^.*desmond.*$)|(^.*charmm.*$)', 'MD')
        # Group all codes that are considered ML codes
        df1['code'] = df1.code.str.replace(r'(^.*python.*$)|(^.*net3.*$)|(^.*imaging.*$)|(^.*dnls.*$)', 'ML')
        # Group all codes that are considered DEM codes
        df1['code'] = df1.code.str.replace(r'(^.*Rocky.*$)', 'DEM')
        # Group all codes that are considered Cryo-EM codes
        df1['code'] = df1.code.str.replace(r'(^.*relion.*$)', 'RELION')
        # Group everything that is not using the GPU
        df1['code'] = df1.code.str.replace(r'(^.*null.*$)', 'NULL')
        # Everything else
        df1['code'] = df1.code.str.replace(r'(^.*a.out.*$)|(^.*lmp.*$)|(^.*nvidia.*$)|(^.* .*$)', 'OTHER')
        # Count the number of times a specific code appears per day and get percentage
        # Remember that GPU400x nodes have 1152 entries per day
        df2 = (df1.groupby(['day', 'code']).size()*100/1152).round(1).reset_index(name='percent')
        appended_data = pd.concat([appended_data, df2], ignore_index=True)
    
    # Get the year and month and store in new column on appended_data dataframe
    appended_data['yearmonth'] = appended_data['day'].astype(str).str[:6]
    
    return appended_data

# Define a function for the main page
def main_page():
    appended_data = load_data()
    
    # Group the data and create the plot using caching
    @st.cache_data
    def create_plot(data):
        grouped_data = data.groupby(['yearmonth', 'code'])['percent'].mean().reset_index()
        
           
        
        fig = px.bar(grouped_data, x='yearmonth', y='percent', color='code', barmode='stack')
    
        fig.update_layout(
            xaxis_title='Year-Month',
            yaxis_title='Percentage',
            title=f'Code Distribution by Month for Last Months ({date.today()})',
            legend_title='Code'
        )
        return fig

    
    fig = create_plot(appended_data)

    # Display the plot using Streamlit
    st.plotly_chart(fig) 
    
    
    
    # Add a "Refresh" button to clear the cache and update data
    # if st.button("Refresh"):
    #     st.runtime.legacy_caching.clear_cache()
    #     st.experimental_rerun()


# Define a function for the "About" page
def table_data():
    st.title("Table Data")
    appended_data = load_data()
    
    @st.cache_data
    def create_data(data):
        grouped_data = data.groupby(['yearmonth', 'code'])['percent'].mean().reset_index()
        st.table(grouped_data.head(20))
        
    create_data(appended_data)
    
    # Add a "Refresh" button to clear the cache and update data
    # if st.button("Refresh"):
    #     st.runtime.legacy_caching.clear_cache()
    #     st.experimental_rerun()
    
# Define a function for the "About" page
def about_page():
    st.title("About")
    st.write("This is an application for analyzing code distribution across different months.")

# Create a dictionary to map page names to their corresponding functions
pages = {
    "Main": main_page,
    "Table": table_data,
    "About": about_page
}

# Add a navigation sidebar
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to", list(pages.keys()))

# Execute the selected page's function
pages[selected_page]()
