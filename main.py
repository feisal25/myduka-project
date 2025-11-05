from flask import Flask, render_template, request, redirect, url_for
from database import fetch_data, insert_products, insert_sales, insert_stock, product_profit, sales_per_product, profit_per_day, sale_per_day, insert_users

#  instance of flask class
app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/products')
def prods():
    prod = fetch_data('products')
    return render_template('products.html', prod=prod)


@app.route('/add_products', methods=['GET', 'POST'])
def add_products():
    # checking method
    if request.method == 'POST':
        # get form input
        pname = request.form['product_name']
        bp = request.form['buying_price']
        sp = request.form['selling_price']
        new_product = (pname, bp, sp)
        # insert to the database
        insert_products(new_product)
    return redirect(url_for('prods'))


@app.route('/stock')
def mystock():
    stoc = fetch_data('stock')
    product = fetch_data('products')
    return render_template('stock.html', stoc=stoc, product=product)


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        PID = request.form['pid']
        quantity = request.form['quantity']
        new_stock = (PID, quantity)
        insert_stock(new_stock)
    return redirect(url_for('mystock'))


@app.route('/sales')
def mysales():
    sal = fetch_data('sales')
    product = fetch_data('products')
    return render_template('sales.html', sal=sal, product=product)


@app.route('/add_sale', methods=['GET', 'POST'])
def add_sale():
    # check http method
    if request.method == 'POST':
        pid = request.form['pid']
        quantity = request.form['quantity']
        new_sale = (pid, quantity)
        # print(new_sale)
        insert_sales(new_sale)
    return redirect(url_for('mysales'))


@app.route('/dashboard')
def dashboard():
    profit = product_profit()
    sale = sales_per_product()
    sale_names = []
    sale_profits = []

    for i in sale:

        sale_names.append(i[0])
        sale_profits.append(float(i[1]))

    product_names = []
    product_profits = []
    for i in profit:
        product_names.append(i[0])
        product_profits.append(float(i[1]))
    # print(product_names)
    sales_d = sale_per_day()
    dates = []
    sales_per_days = []
    for i in sales_d:
        dates.append(str(i[0]))
        sales_per_days.append(float(i[1]))

    profit = profit_per_day()
    sale_date = []
    daily_profit = []
    for i in profit:
        sale_date.append(str(i[0]))
        daily_profit.append(float(i[1]))

    return render_template('dashboard.html', product_names=product_names,
                           product_profits=product_profits, sale_names=sale_names, sale_profits=sale_profits,
                           dates=dates, sales_per_days=sales_per_days, sale_date=sale_date, daily_profit=daily_profit)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname=request.form['full_name']
        email=request.form['email']
        password=request.form['password']
        new_user=(fname,email,password)
        insert_users(new_user)
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


app.run(debug=True)
