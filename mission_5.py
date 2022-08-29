"""
@author: jamison.queiroz
Size: 1,25 kB
Type: Python
Modified: 02/08/2022 22:06
Created: 25/07/2022 21:24
"""
#-----------------------------------------------------------------------------------------------------------------------
# Bibliotecas Necessárias
#-----------------------------------------------------------------------------------------------------------------------
from faker import Faker
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import pandas as pd
import numpy as np
from num2words import num2words
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
#-----------------------------------------------------------------------------------------------------------------------
# Classe Dashboard
#-----------------------------------------------------------------------------------------------------------------------
class Dashboard:
    def __init__(self, num_alunos):
        self.num_alunos = num_alunos
        self.lista_dic = []

    def gerar_dados(self):
        self.faker = Faker()
        for x in range(self.num_alunos):
            self.aluno = dict(zip(['Nome', 'Nota'], [self.faker.name(), self.faker.random_int(1, 10)]))
            self.lista_dic.append(self.aluno)

    def exibir_dados(self):
        print(f"{'NOME': <24} | {'NOTA': <2}")
        print("--------------------------------------")
        for x in self.lista_dic:
           print(f"{x['Nome']: <24} {x['Nota']: <2}")

    def gerar_csv(self):
        self.csv_colunas = ['Nome', 'Nota']
        self.arquivo_csv = "notas_alunos.csv"
        try:
            with open(self.arquivo_csv, "w", newline='') as arquivo:
                self.writer = csv.DictWriter(arquivo, fieldnames=self.csv_colunas)
                self.writer.writeheader()
                for data in self.lista_dic:
                    self.writer.writerow(data)
        except IOError:
            print("Error ao gerar o arquivo CSV")

    def gerar_grafico(self):
        self.data = pd.read_csv('notas_alunos.csv')
        plt.figure(figsize=(8, 6))
        plt.hist(self.data['Nota'], weights=np.ones(len(self.data['Nota'])) / len(self.data['Nota']), color='#2DB200')
        plt.ylabel('Probabilidade')
        plt.xlabel('Pontuação')
        plt.title('Histograma de Pontuações')
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        plt.show()

    def gerar_wordcloud(self):
        # concatenar as palavras
        self.nome_notas = ",".join(s for s in self.data['Nota'].apply(num2words))
        # lista de stopword
        self.stopwords = set(STOPWORDS)
        self.stopwords.update([","])
        self.mask = np.array(Image.open('gato.jpg'))  # nome do arquivo da imagem
        self.mask_colors = ImageColorGenerator(self.mask)
        self.wc = WordCloud(stopwords=self.stopwords,
                       mask=self.mask, background_color="white",
                       max_words=2000, max_font_size=256,
                       random_state=42, width=self.mask.shape[1],
                       height=self.mask.shape[0], color_func=self.mask_colors)
        self.wc.generate(self.nome_notas)
        plt.imshow(self.wc, interpolation="bilinear")
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    d = Dashboard(30)
    d.gerar_dados()
    d.exibir_dados()

    d.gerar_csv()
    d.gerar_grafico()
    d.gerar_wordcloud()