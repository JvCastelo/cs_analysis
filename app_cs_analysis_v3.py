import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import plotly.express as px
from PIL import Image

icon_image = Image.open('icon_cs_analysis.jpg')

st.set_page_config(page_title='CS Analysis',
                   page_icon=icon_image,
                   layout='wide')

st.title("Costumer Success Analysis")

uploaded_file = st.file_uploader(label='Choose a file', 
                                 type='csv', 
                                 help='Upload your file for analysis. Only supports .csv files.')

if uploaded_file is not None:
    with st.container():

        df_tickets_raw = pd.read_csv(uploaded_file)
        st.header('Dataset Raw')
        st.dataframe(df_tickets_raw)

    with st.container():

        st.header('Setting Period')

        input_start_date_analysis = st.date_input(label='Start Date Analysis', 
                                        value=(datetime.today() + timedelta(days=-1)))

        start_date_analysis = datetime.combine(input_start_date_analysis, datetime.min.time())

        input_end_date_analysis = st.date_input(label='End Date Analysis', 
                                        value=datetime.today())

        end_date_analysis = datetime.combine(input_end_date_analysis, datetime.max.time())

    df_tickets_raw.drop(['comentario', 'data_comentario'], axis=1, inplace=True)

    df_tickets_raw['inicio_ticket'] = pd.to_datetime(df_tickets_raw['inicio_ticket'])
    df_tickets_raw['dia_atual'] = pd.to_datetime(df_tickets_raw['dia_atual'])
    df_tickets_raw['fim_ticket'] = pd.to_datetime(df_tickets_raw['fim_ticket'])
    df_tickets_raw['numero_ticket'] = df_tickets_raw['numero_ticket'].astype('int32')
    df_tickets_raw['duracao_ticket'] = df_tickets_raw['duracao_ticket'].astype('int32')

    filtering_period_open = (df_tickets_raw['inicio_ticket'] >= start_date_analysis) & (df_tickets_raw['inicio_ticket'] <= end_date_analysis) 

    df_tickets_filtered_open = df_tickets_raw[filtering_period_open]

    df_tickets_filtered_count_client_open = df_tickets_filtered_open.groupby('cliente').count()
    df_tickets_filtered_count_client_open.drop(list(df_tickets_filtered_count_client_open)[1:], axis=1, inplace=True)
    df_tickets_filtered_count_client_open.rename(columns={'nome_ticket' : 'quantidade_ticket'}, inplace=True)
    df_tickets_filtered_count_client_open.sort_values(by=['quantidade_ticket'], inplace=True, ascending=False)
    df_tickets_filtered_count_client_open.reset_index(inplace=True)
    
    filtering_period_solve = (df_tickets_raw['fim_ticket'] >= start_date_analysis) & (df_tickets_raw['fim_ticket'] <= end_date_analysis) 

    df_tickets_filtered_solve = df_tickets_raw[filtering_period_solve]

    df_tickets_filtered_count_client_solve = df_tickets_filtered_solve.groupby('cliente').count()
    df_tickets_filtered_count_client_solve.drop(list(df_tickets_filtered_count_client_solve)[1:], axis=1, inplace=True)
    df_tickets_filtered_count_client_solve.rename(columns={'nome_ticket' : 'quantidade_ticket'}, inplace=True)
    df_tickets_filtered_count_client_solve.sort_values(by=['quantidade_ticket'], inplace=True, ascending=False)
    df_tickets_filtered_count_client_solve.reset_index(inplace=True)
    
    with st.container():
        st.header('Dataset Filtered')
        
        st.write('Opened Tickets')
        st.dataframe(df_tickets_filtered_count_client_open)
        
        st.write('Solved Tickets')
        st.dataframe(df_tickets_filtered_count_client_solve)
        
    df_tickets_filtered_count_client_open.sort_values('quantidade_ticket', ascending = True, inplace=True)
    df_tickets_filtered_count_client_solve.sort_values('quantidade_ticket', ascending = True, inplace=True)

    with st.container():

        fig_open = px.bar(data_frame =df_tickets_filtered_count_client_open, 
                    x='quantidade_ticket', 
                    y='cliente',
                    color='cliente',
                    title='Quantidade de Chamados Iniciados no período de '+start_date_analysis.strftime("%d/%m/%Y")+' a '+end_date_analysis.strftime("%d/%m/%Y")
                    )
        
        st.plotly_chart(fig_open, use_container_width=True, theme='streamlit')

        fig_solve = px.bar(data_frame =df_tickets_filtered_count_client_solve, 
                    x='quantidade_ticket', 
                    y='cliente',
                    color='cliente',
                    title='Quantidade de Chamados Finalizados no período de '+start_date_analysis.strftime("%d/%m/%Y")+' a '+end_date_analysis.strftime("%d/%m/%Y")
                    )
        
        st.plotly_chart(fig_solve, use_container_width=True, theme='streamlit')

else:
    st.write('Please, upload your file to continue.')
