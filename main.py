from flask import Flask ,render_template
from database import fetch_data

#  instance of flask class
app=Flask(__name__) 

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/products')
def prods():
    prod=fetch_data('products')
    return  render_template('products.html', prod=prod)


@app.route('/stock')
def mystock():
    stoc=fetch_data('stock')
    return  render_template('stock.html',stoc=stoc)


@app.route('/sales')
def sales():
    sal=fetch_data('sales')
    return  render_template('sales.html',sal=sal)


app.run()
