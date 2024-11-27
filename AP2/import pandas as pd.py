# Instalar as bibliotecas necessárias
!pip install flask-ngrok pandas matplotlib seaborn

# Criar arquivo CSV no ambiente
dados = """
Descricao_produto,Preco_a_vista,Valor_parcelado
Placa de Video RTX 4060 VENTUS 2x Black OC MSI NVIDIA GeForce, 8GB GDDR6, DLSS, Ray Tracing,1945.99,2262.70
Placa de Video RTX4060 1-Click OC 2X TecLab Lite GALAX NVIDIA GeForce, 8GB GDDR6, G-SYNC, DLSS, Ray Tracing,1899.99,223
Placa de Video RTX 4060 EAGLE OC Gigabyte NVIDIA GeForce, 8GB GDDR6, DLSS, Ray Tracing,2099,
Placa de Video RTX 4060 TI Ventus 2X Black 8G OC MSI NVIDIA GeForce, 8GB GDDR6, DLSS, Ray Tracing, G-Sync,2549.99,2999
Placa de Video RTX 4060 8G V2 Gaming ATS OC ASUS NVIDIA GeForce, 8GB GDDR6, DLSS, Ray Tracing, G-Sync,,
"""

# Salvar o arquivo de dados
with open("dados.csv", "w") as f:
    f.write(dados)

# Importar bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, jsonify
from flask_ngrok import run_with_ngrok

# Ler os dados
df = pd.read_csv("dados.csv")

# Tratar valores ausentes e converter preços
df["Preco_a_vista"] = pd.to_numeric(df["Preco_a_vista"], errors="coerce").fillna(0)
df["Valor_parcelado"] = pd.to_numeric(df["Valor_parcelado"], errors="coerce").fillna(0)

# Gerar gráficos para análise univariada
def gerar_graficos_univariados():
    # Histograma
    plt.figure(figsize=(10, 6))
    plt.hist(df["Preco_a_vista"], bins=10, color='blue', alpha=0.7)
    plt.title("Histograma - Preço à Vista")
    plt.xlabel("Preço à Vista")
    plt.ylabel("Frequência")
    plt.show()

    # Boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df["Preco_a_vista"], color='green')
    plt.title("Boxplot - Preço à Vista")
    plt.xlabel("Preço à Vista")
    plt.show()

    # Gráfico de barras
    plt.figure(figsize=(10, 6))
    df['Descricao_produto'].value_counts().head(10).plot(kind='bar', color='purple')
    plt.title("Top 10 Produtos mais caros")
    plt.xlabel("Produto")
    plt.ylabel("Frequência")
    plt.show()

    # Gráfico de pizza
    plt.figure(figsize=(10, 6))
    df['Descricao_produto'].value_counts().head(10).plot(kind='pie', autopct='%1.1f%%')
    plt.title("Distribuição de Produtos (Top 10)")
    plt.ylabel("")
    plt.show()

# Gerar gráficos para análise multivariada
def gerar_graficos_multivariados():
    # Gráfico de dispersão
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df["Preco_a_vista"], y=df["Valor_parcelado"], hue=df["Descricao_produto"], palette='viridis')
    plt.title("Gráfico de Dispersão - Preço à Vista vs Valor Parcelado")
    plt.xlabel("Preço à Vista")
    plt.ylabel("Valor Parcelado")
    plt.show()

    # Boxplot Multivariado
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df["Descricao_produto"], y=df["Preco_a_vista"], palette='Set3')
    plt.title("Boxplot Multivariado - Preço por Produto")
    plt.xlabel("Produto")
    plt.ylabel("Preço à Vista")
    plt.xticks(rotation=90)
    plt.show()

    # Gráfico de barras Multivariado
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Descricao_produto", y="Preco_a_vista", data=df, estimator=sum, ci=None, palette='coolwarm')
    plt.title("Gráfico de Barras Multivariado - Preço por Produto")
    plt.xlabel("Produto")
    plt.ylabel("Soma do Preço à Vista")
    plt.xticks(rotation=90)
    plt.show()

# Iniciar o servidor Flask
app = Flask(__name__)
run_with_ngrok(app)

@app.route("/")
def index():
    # Exibir os dados no formato JSON
    return jsonify(df.to_dict(orient="records"))

@app.route("/grafico_univariado")
def grafico_univariado():
    gerar_graficos_univariados()
    return "Gráficos Univariados Gerados!"

@app.route("/grafico_multivariado")
def grafico_multivariado():
    gerar_graficos_multivariados()
    return "Gráficos Multivariados Gerados!"

# Iniciar o servidor
app.run()
