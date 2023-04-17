from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd
import matplotlib.pyplot as plt
import os
df = pd.read_excel("https://github.com/wtitze/3E/blob/main/BikeStores.xls?raw=true", sheet_name='products')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/categoria')
def categoria():
    categorie = list(set(df["category_id"]))
    categorie.sort()
    return render_template('categoria.html', lista = categorie)

@app.route('/risultatoCategoria', methods = ["GET"])
def risultatocategoria():
    cat = int(request.args.get("categoria"))
    df1 = df[df["category_id"] == cat].sort_values(by="product_name").to_html()
    return render_template('tabella.html', tabella = df1)

@app.route('/prezzo')
def prezzo():
    return render_template('prezzo.html')

@app.route('/risultatoPrezzo', methods = ["GET"])
def risultatoprezzo():
    minimmo = int(request.args.get("minimo"))
    massimo = int(request.args.get("massimo"))
    df2 = df[(df["list_price"] >= minimmo) & (df["list_price"] <= massimo)].sort_values(by="list_price", ascending = False).to_html()
    return render_template('tabella.html', tabella = df2)

@app.route('/stringa')
def stringa():
    return render_template('stringa.html')


@app.route('/risultatoStringa', methods = ["GET"])
def risultatostringa():
    parola = request.args.get("parola")
    df3 = df[df["product_name"].str.contains(parola)].sort_values(by="product_name").to_html()
    return render_template('tabella.html', tabella = df3)

@app.route('/prodotti')
def prodotti():
    df4 = df.groupby("category_id").count()[["product_name"]].sort_values(by="product_name", ascending = False).reset_index().to_html()
    return render_template('tabella.html', tabella = df4)

@app.route('/grafico')
def grafico():
    gr = df.groupby("category_id").count()[["product_name"]].sort_values(by="product_name", ascending = False).reset_index()
    x = gr["product_name"]
    y = gr["category_id"]
    plt.bar(y, x, color = ["red", "blue", "green"])
    plt.title('numero di prodotti per ogni categoria')
    plt.xlabel('categorie')
    plt.ylabel('nProdotti')
    plt.subplots_adjust(bottom=0.25)
    dir = "static/images"
    file_name = "graf.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template('grafico.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)