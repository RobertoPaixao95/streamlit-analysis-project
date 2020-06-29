import pandas as pd
import plotly.express as px
import streamlit as st

def main():

    st.image('img\logo.png', width=700)
    st.title('ANÁLISE EXPLORATÓRIA DE DADOS')
    st.subheader('Você poderá fazer exploração de dados de forma simples.')
    data = st.file_uploader('Carregue seu .csv', type='csv')

    if data is not None:
        df = pd.read_csv(data, sep=',')
        
        st.sidebar.image('img/data_analysis.jpg', width=300)
        st.sidebar.markdown('#### Selecione o que deseja ver')
        opcao = st.sidebar.radio('',(['Informações','Gráficos']))

        if opcao == 'Informações':
            
            st.markdown('#### DIMENSÕES DO DATASET')
            st.write(f'**Linhas**: {df.shape[0]} | **Colunas**: {df.shape[1]}')

            st.markdown('#### TIPOS DE VARIÁVEIS DAS COLUNAS')
            st.text(df.dtypes)

            st.markdown('#### Primeiras linhas do Dataset')
            st.dataframe(df.head())

            st.markdown('#### Últimas linhas do Dataset')
            st.dataframe(df.tail())
            
            st.markdown('#### Quantidade de valores faltantes do Dataset')
            st.text(df.isnull().sum())
            porcentagem_faltante = df.isnull().mean()
            total_faltante = df.isnull().sum()
            st.text(f'Total faltante: {total_faltante.sum()} ({porcentagem_faltante.sum():.2f}%)')
             
            

            st.markdown('#### Estatísticas Descritivas')
            st.dataframe(df.describe().T)

        elif opcao == 'Gráficos':
            # Coletando colunas por tipos.
            colunas_num = df.select_dtypes(['int', 'float']).columns.tolist()
            colunas_obj = df.select_dtypes(['object']).columns.tolist()

            st.markdown('## HISTOGRAMA')
            opcoes_colunas_num = st.selectbox('Distribuição da variável.', colunas_num)
            histograma = px.histogram(df, x=opcoes_colunas_num)
            st.plotly_chart(histograma)

            st.markdown('## CORRELAÇÕES')
            obj_x = st.selectbox('Eixo X:', colunas_num)
            obj_y = st.selectbox('Eixo Y:', colunas_num)
            scatter = px.scatter(df, x=obj_x, y=obj_y)
            st.plotly_chart(scatter)

            st.markdown('## GRÁFICO DE BARRAS')
            opcoes_colunas_obj = st.selectbox('Selecione a coluna desejada:', colunas_obj)
            plot_barras = px.bar(x = df[opcoes_colunas_obj].value_counts().index,
                                 y = df[opcoes_colunas_obj].value_counts().values,
                                 )
            st.plotly_chart(plot_barras)


if __name__ == '__main__':
    main()

    