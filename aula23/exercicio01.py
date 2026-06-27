import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

try:
    print('Obtendo os dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    df_recuperacoes = df_ocorrencias[['cisp', 'recuperacao_veiculos']]

    df_recuperacoes = df_recuperacoes.groupby('cisp', as_index=False)['recuperacao_veiculos'].sum()

    df_recuperacoes = df_recuperacoes.sort_values(by='recuperacao_veiculos', ascending=False)

    # print(df_recuperacoes)
    print(df_recuperacoes.head(10))

except Exception as e:
    print(f'Erro ao obter dados {e}')

# Obtendo a medidas
try:
    print('Calculando as medidas... ')
    array_recuperacoes = np.array(df_recuperacoes['recuperacao_veiculos'])

    media_recuperacoes = np.mean(array_recuperacoes)
    mediana_recuperacoes = np.median(array_recuperacoes)


    distancia = abs((media_recuperacoes - mediana_recuperacoes) / mediana_recuperacoes * 100)

    print('\nMedidas de Tendência Central')
    print(30*"=")
    print(f'Média: {media_recuperacoes}')
    print(f'Mediana: {mediana_recuperacoes}')
    print(f'Distancia: {distancia} %')

except Exception as e:
    print(f'Erro ao processar as medidas {e}')

try:
    print('Processando os quartis')

    q1 = np.quantile(array_recuperacoes, .25)
    q3 = np.quantile(array_recuperacoes, .75)

    print('\nQuartis')
    print(30*"=")
    print(f'Q1: {q1}')
    print(f'Mediana: {media_recuperacoes}')
    print(f'Q3: {q3}')

    df_recuperacoes_menores = df_recuperacoes[df_recuperacoes['recuperacao_veiculos'] < q1]
    df_recuperacoes_maiores = df_recuperacoes[df_recuperacoes['recuperacao_veiculos'] > q3]

    print('\nDelegacias com menos casos de recuperação de veículos')
    print(30*"=")
    print(df_recuperacoes_menores.sort_values(by='recuperacao_veiculos', ascending=True))

    print('\nDelegacias com maiores casos de recuperação de veículos')
    print(30*"=")
    print(df_recuperacoes_maiores)

except Exception as e:
    print(f'Erro ao obter a distribuição {e}')  

try:
    maximo = np.max(array_recuperacoes)
    minimo = np.min(array_recuperacoes)
    amplitude = maximo - minimo

    print('\nMedidas de Disperção')
    print(30*"=")
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude Total: {amplitude}')

except Exception as e:
    print(f'Erro ao calcular medidas de dispersão: {e}')

try:
    iqr = q3 - q1
    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)

    print('\nMedidas ')
    print(30*"=")
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Mediana: {mediana_recuperacoes}')  # q2
    print(f'Q3: {q3}')
    print(f'Limite superior: {limite_superior}')
    print(f'Máximo: {maximo}')    

except Exception as e:
    print(f'Erro ao calcular os limites: {e}')

try:
    df_recuperacoes_outliers_superiores = df_recuperacoes[df_recuperacoes['recuperacao_veiculos'] > limite_superior]
    df_recuperacoes_outliers_inferiores = df_recuperacoes[df_recuperacoes['recuperacao_veiculos'] < limite_inferior]

    print('\nDelegacias com Outliers Inferiores ')
    print(30*"=")
    if len(df_recuperacoes_outliers_inferiores) == 0:
        print('Não existe outliers inferiores')
    else:
        print(df_recuperacoes_outliers_inferiores.sort_values(by='recuperacao_veiculos', ascending=True))

    print('\nDelegacias com Outliers Superiores ')
    print(30*"=")
    if len(df_recuperacoes_outliers_superiores) == 0:
        print('Não existe outliers superiores')
    else: 
        print(df_recuperacoes_outliers_superiores.sort_values(by='recuperacao_veiculos', ascending=False))

except Exception as e:
    print(f'Erro ao Calular Outliers {e}')

try:
    assimetria = df_recuperacoes['recuperacao_veiculos'].skew()
    curtose = df_recuperacoes['recuperacao_veiculos'].kurtosis()
    print('\nMedidas de Distribuição')
    print(30*"=")
    print(f'Assimetria: {assimetria}')
    print(f'Curtose: {curtose}')

except Exception as e:
    print(f'Erro ao calcular medidas de distribuição {e}') 

try:
    print('Calculando a variabilidade dos dados')
    variancia = np.var(array_recuperacoes)
    distancia_var_media = variancia / (media_recuperacoes ** 2) * 100
    desvio_padrao = np.std(array_recuperacoes)
    coef_variacao = desvio_padrao / media_recuperacoes

    print('\nMedidas de Variabilidade')
    print(30*"=")
    print(f'Variância: {variancia}')
    print(f'Distância entre Variância e a Média: {distancia_var_media} %')
    print(f'Desvio Padrão: {desvio_padrao}')
    print(f'Coeficiente de Variação: {coef_variacao}')

except Exception as e:
    print(f'Erro ao calcular a variabilidade dos dados: {e}')  

try:
    # 01
    plt.subplot(2, 2, 1)
    plt.boxplot(array_recuperacoes,vert=False,showmeans=True)
    plt.title('Boxplot da Distribuição')

    # 02
    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.9, f'Média: {media_recuperacoes}', fontsize=9)
    plt.text(0.1, 0.8, f'Distância: {distancia}', fontsize=9)
    plt.text(0.1, 0.7, f'Limite Inferior: {limite_inferior}', fontsize=9)
    plt.text(0.1, 0.6, f'Mínimo: {minimo}', fontsize=9)      
    plt.text(0.1, 0.5, f'Q1: {q1}', fontsize=9)
    plt.text(0.1, 0.4, f'Mediana: {mediana_recuperacoes}', fontsize=9)
    plt.text(0.1, 0.3, f'Q3: {q3}', fontsize=9)
    plt.text(0.1, 0.2, f'Limite Superior: {limite_superior}', fontsize=9)
    plt.text(0.1, 0.1, f'Máximo: {maximo}', fontsize=9)
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude}', fontsize=9)

    plt.axis('off')
    plt.title('Resumo Estatístico')

    # 03
    plt.subplot(2, 2, 3)
    df_recuperacoes_outliers_superiores = (df_recuperacoes_outliers_superiores.head(10).sort_values(by='recuperacao_veiculos', ascending=False))

    plt.bar(df_recuperacoes_outliers_superiores['cisp'],
        df_recuperacoes_outliers_superiores['recuperacao_veiculos'] 
     )

    deslocamento = max(df_recuperacoes_outliers_superiores['recuperacao_veiculos']) * 0.02
    
    for i, valor in enumerate(df_recuperacoes_outliers_superiores['recuperacao_veiculos']):
         plt.text(
             i,
            valor + deslocamento,
             f'{valor:,}',
             ha='center'
         )
        
    plt.xticks(rotation=45, ha='right')
    plt.title('Outliers Superiores')

    #04
    plt.subplot(2, 2, 4)
    plt.hist(array_recuperacoes, bins=100)
    plt.axvline(media_recuperacoes, color='green', linewidth=1)
    plt.axvline(mediana_recuperacoes, color='orange', linewidth=1)
    plt.title('Histograma da Distribuição')

    

    plt.tight_layout() 
    plt.show()


    plt.show()

except Exception as e:
    print(f'Erro ao plotar o gráfico: {e}')

print('Os dados apresentam alta disperção e não possuem um padrão predominante')
print('Sim, foram identificados delegacias com maior recuperação de veículos que outras, entre elas temos as DP: 59, 39, 21, 64, 34, 72, 54, 38 e 27')
print('As delegacias 59, 39, 21 e 64 são as que recuperaram mais veículos, enquanto as delegacias 45, 92, 138 e 155 foram as que tiveram menor indice de recuperação')
print('Pelos dados apresentados, poucas delegacias recuperam muitos veiculos, enquanto a maioria uma quantidade menor, dessa forma, não existe um padrão de recuperação igual entre todas as delegacias.')

