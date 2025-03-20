import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import time

st.set_page_config(
    page_title="Streamlit App",
    page_icon='📊'
)

# Title
st.title(":rainbow[Data Analytics Portal]")
st.subheader(":gray[Explore Data with ease]", divider='rainbow')

file = st.file_uploader('Drop csv or excel file', type=['csv', 'xlsx'])
if file is not None:
    if file.name.endswith('csv'):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)
        
    st.dataframe(data)
    st.info("File is successfully uploaded")
    
    st.subheader(":rainbow[Basic Information of the Dataset]", divider='rainbow')
    tab1, tab2, tab3, tab4 = st.tabs(['Summary', 'Top and Bottom Rows', 'Data Types', 'Columns'])
    
    with tab1:
        st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset.')
        st.subheader(':gray[Statistical Summary of the Dataset]')
        st.dataframe(data.describe())
        
    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows = st.slider('Number of rows to display', 1, data.shape[0], key='topslider') 
        st.dataframe(data.head(toprows))
        st.subheader(':gray[Bottom Rows]')
        bottomrows = st.slider('Number of rows to display', 1, data.shape[0], key='bottomslider') 
        st.dataframe(data.tail(bottomrows))  
        
    with tab3:
        st.subheader(':gray[Data Types of Columns]')    
        st.dataframe(data.dtypes)
        
    with tab4:
        st.subheader('Column Names in Dataset')    
        st.write(list(data.columns))
        
    st.subheader(':rainbow[Column Values to Count]', divider='rainbow')
    with st.expander("Value Count"):
        col1, col2 = st.columns(2)
        with col1:
            columns = st.selectbox("Choose Column", options=list(data.columns))    
        with col2:    
            toprows = st.number_input('Top rows', min_value=1, step=1)
            
        count = st.button("Count")
        if count:
            result = data[columns].value_counts().reset_index().head(toprows)
            st.dataframe(result)    
            st.subheader("Visualization", divider="gray")
            fig = px.bar(data_frame=result, x=columns, y='count', text='count', template="plotly_white")
            st.plotly_chart(fig)
            fig = px.line(data_frame=result, x=columns, y="count", text="count", template="plotly_white")
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result, names=columns, values="count")
            st.plotly_chart(fig)
            
    st.subheader(":rainbow[Groupby : Simplify Your Data Analysis]", divider="rainbow")        
    st.write("The groupby function allows you to summarize data by specific categories and groups.")
    
    with st.expander("Group By Your Columns"):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect("Choose your column(s) to group by", options=list(data.columns))
        with col2:
            operation_col = st.selectbox("Choose column for operation", options=list(data.columns))
        with col3:
            operation = st.selectbox("Choose operation", options=['sum', 'max', 'min', 'mean', 'median', 'count'])
    
        if groupby_cols:
            # Map the operation string to the corresponding pandas function
            operations_map = {
                'sum': np.sum,
                'max': np.max,
                'min': np.min,
                'mean': np.mean,
                'median': np.median,
                'count': 'count'
            }
            agg_func = operations_map.get(operation, 'sum')  # Default to sum if not found
            
            # Apply the groupby and aggregation
            result = data.groupby(groupby_cols).agg(
                newcol=(operation_col, agg_func)
            ).reset_index()
            
            st.dataframe(result)
            
            st.subheader(":gray[Data Visualization]", divider="gray")
            graphs = st.selectbox("Choose Your Graph", options=['line', 'bar', 'scatter', 'pie', 'sunburst'])
            
            if graphs == 'line':
                x_axis = st.selectbox("Choose X axis", options=list(result.columns))
                y_axis = st.selectbox("Choose Y axis", options=list(result.columns))
                color = st.selectbox("Color Information", options=[None] + list(result.columns))
                fig = px.line(data_frame=result, x=x_axis, y=y_axis, color=color, markers='o')
                st.plotly_chart(fig)
            elif graphs == 'bar':
                x_axis = st.selectbox("Choose X axis", options=list(result.columns))
                y_axis = st.selectbox("Choose Y axis", options=list(result.columns))
                color = st.selectbox("Color Information", options=[None] + list(result.columns))
                facet_col = st.selectbox("Column Information", options=[None] + list(result.columns))
                fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode="group")
                st.plotly_chart(fig)
            elif graphs == 'scatter':
                x_axis = st.selectbox("Choose X axis", options=list(result.columns))
                y_axis = st.selectbox("Choose Y axis", options=list(result.columns))
                color = st.selectbox("Color Information", options=[None] + list(result.columns))
                size = st.selectbox("Size Column", options=[None] + list(result.columns))
                fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color, size=size)
                st.plotly_chart(fig)
            elif graphs == 'pie':
                values = st.selectbox("Choose Numerical Values", options=list(result.columns))
                names = st.selectbox("Choose Labels", options=list(result.columns))
                fig = px.pie(data_frame=result, names=names, values=values)
                st.plotly_chart(fig)
            elif graphs == 'sunburst':
                path = st.multiselect("Choose Your Path", options=list(result.columns))
                fig = px.sunburst(data_frame=result, path=path)
                st.plotly_chart(fig)
