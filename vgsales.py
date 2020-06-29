import streamlit as st
import pandas as pd 
import plotly.figure_factory as ff
import plotly.graph_objects as go


def main():
    
    # - - - - - - HEADER - - - - - - - #
    st.image('img\logo.png', width=700)
    st.title('VGSales - Exploratory Data Analysis (EDA)')
    st.subheader('Análise do dataset com dados históricos sobre vendas de jogos eletrônicos.')
    # ----------------------------------

    # - - - - - - LOAD FILE - - - - -  #
    df = pd.read_csv('vgsales.csv')

    # - - - - - - SIDE OPTIONS - - - - #
    opcao = st.sidebar.selectbox(
        "Opções:",
        ('Informações',
         'Gráficos')
    )
    
    if opcao == 'Informações':
        # - - - - - - ANALYSIS - - - - - - #
        # INFO DO DATASET
        st.markdown('## INFORMAÇÕES SOBRE O DATASET')
        
        st.markdown('#### DIMENSÕES DO DATASET')
        st.write('Linhas: ', df.shape[0], 'Colunas: ', df.shape[1])
        
        st.markdown('#### VALORES FALTANTES')
        st.text(df.isnull().sum())
        
        # TIPO DE VARIÁVEIS DAS COLUNAS
        st.markdown('#### COLUNAS E SEUS TIPOS DE VARIÁVEIS.')
        tipo_colunas = df.dtypes
        st.text(tipo_colunas)

        # OBSERVANDO O DATASET E SUAS LINHAS 
        st.markdown('#### QUANTAS LINHAS DESEJA OBSERVAR? (1 - 50)')
        slider = st.slider('Linhas: ', 1, 50)

        # HEAD 
        st.markdown('#### PRIMEIRAS LINHAS DO DATASET')
        st.table(df.head(slider))

        # TAIL
        st.markdown('#### ÚLTIMAS LINHAS DO DATASET') 
        st.table(df.tail(slider))

        # ESTATISTICA DESCRITIVAS DO DF (DESCRIBE)
        st.markdown('#### ESTATÍSTICAS DESCRITIVA DO DATASET')
        st.table(df.describe().T)
    
    elif opcao == 'Gráficos':
        # DISTRIBUIÇÃO DOS GÊNEROS ENTRE AS PLATAFORMAS
        st.markdown('## GRÁFICOS SOBRE O DATASET')
        st.plotly_chart(qtde_produzida_por_genero(df))
        st.plotly_chart(top_plataformas(df))
        st.plotly_chart(dist_generos_x_plat(df))
    
    
# Distribuição dos Gêneros entre as Plataformas
def dist_generos_x_plat(df):
    st.markdown('#### DISTRIBUIÇÃO DOS GÊNEROS ENTRE AS PLATAFORMAS')
    dist_plataforma = pd.crosstab(df['Platform'], df['Genre'])

    fig = ff.create_annotated_heatmap(dist_plataforma.T.values,
                                  x = list(dist_plataforma.index), 
                                  y = list(dist_plataforma.columns),
                                  font_colors = ['Black', 'White'],
                                  colorscale = 'Magma',
                                  reversescale = True,
                                  showscale = True,
                                  )
                                  
    fig.update_layout(width=1000, height=500)

    return fig

# Quantidade de jogos produzidos por Gênero
def qtde_produzida_por_genero(df):
    st.markdown('#### QUANTIDADE DE JOGOS PRODUZIDOS POR GÊNERO')
    gen = df.Genre.value_counts(sort = False)
    gen_mean = gen.mean()
    max_gen = gen.values.max()

    colors = []
    cor_width = []

    for x, y in zip(gen.values, gen.index):
        if x == max_gen:
            gen_max = y
            colors.append('MediumSeaGreen')
            cor_width.append('LightGreen')
        elif x >= gen_mean:
            colors.append('SteelBlue')
            cor_width.append('RoyalBlue')
        else:
            colors.append('LightBlue')
            cor_width.append('RoyalBlue')

    trace = go.Bar(x = gen.index,
                y = gen.values,
                showlegend = False,
                marker = {'color': colors,
                          'line' : {'color': cor_width,
                                    'width': 1}})

    layout = go.Layout(title='Quantidade de Jogos produzidos por Gênero.',
                       xaxis=dict(title='Gêneros'),
                       yaxis=dict(title='Quantidade de Jogos'),
                       annotations=[{'text': 'Gênero de Destaque',
                                       'x':gen_max,
                                       'y':max_gen}],
                        width=1000,
                        height=500)

    data = [trace]
    fig = go.Figure(data = data, layout = layout)
    return fig

# As 5 Plataformas com maior quantidade de Jogos.
def top_plataformas(df):
    st.markdown('#### AS 5 PLATAFORMAS COM MAIOR QUANTIDADE DE JOGOS.')
    platform_vend = df.Platform.value_counts(sort = False)
    max_plat = df.Platform.value_counts().head()

    colors = []
    colors_width = []

    for x, y in zip(platform_vend.values, platform_vend.index):
        if x >= 1200:
            colors.append('MediumSeaGreen')
            colors_width.append('Teal')
        else: 
            colors.append('SteelBlue')
            colors_width.append('RoyalBlue')
                
    #Plot

    trace = go.Bar(
            x=platform_vend.index,
            y=platform_vend.values,
            marker = {'color': colors,
                      'line':{'color': colors_width,
                              'width': 1}})

    lt = go.Layout(
        title='As 5 Plataformas com maior quantidade de Jogos.',
        xaxis=dict(title='Plataformas'),
        yaxis=dict(title='Jogos Produzidos'),
        width=1000,
        height=500)

    data = [trace]

    fig = go.Figure(data = data, layout = lt)
    return fig



if __name__ == '__main__':
    main()