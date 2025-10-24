from flask import Flask ,render_template

#  instance of flask class
app=Flask(__name__) 

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/products')
def prods():
    return  render_template('products.html')


@app.route('/stock')
def mystock():
    return  render_template('stock.html')


@app.route('/sales')
def sales():
    return  render_template('sales.html')


app.run()
