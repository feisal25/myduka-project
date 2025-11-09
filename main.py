from flask import Flask, render_template, request, redirect, url_for,session,flash
from database import fetch_data, insert_products, insert_sales, insert_stock, product_profit, sales_per_product, profit_per_day, sale_per_day, insert_users, check_email
from flask_bcrypt import Bcrypt

#  instance of flask class
app = Flask(__name__)
bcrypt=Bcrypt(app)

app.secret_key='wertyuiocnmdfghj'


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/products')
def prods():
    if session.get('email'):
        prod = fetch_data('products')
        return render_template('products.html', prod=prod)
    else:
        flash('login to access this page')
        return redirect(url_for('login'))


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
        flash('product added successful')
    return redirect(url_for('prods'))


@app.route('/stock')
def mystock():
    if session.get('email'):
        stoc = fetch_data('stock')
        product = fetch_data('products')
        return render_template('stock.html', stoc=stoc, product=product)
    else:
        flash('login to access this page')
        return redirect(url_for('login'))


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        PID = request.form['pid']
        quantity = request.form['quantity']
        new_stock = (PID, quantity)
        insert_stock(new_stock)
        flash('stock added successful')
    return redirect(url_for('mystock'))


@app.route('/sales')
def mysales():
    if session.get('email'):
        sal = fetch_data('sales')
        product = fetch_data('products')
        return render_template('sales.html', sal=sal, product=product)
    else:
        flash('login to access this page')
        return redirect(url_for('login'))


@app.route('/add_sale', methods=['GET', 'POST'])
def add_sale():
    # check http method
    if request.method == 'POST':
        pid = request.form['pid']
        quantity = request.form['quantity']
        new_sale = (pid, quantity)
        # print(new_sale)
        insert_sales(new_sale)
        flash('sale made successfully' )
    return redirect(url_for('mysales'))


@app.route('/dashboard')
def dashboard():
    if session.get('email'):
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
    else:
        flash('login to access this page')
        return redirect(url_for('login'))

    return render_template('dashboard.html', product_names=product_names,
                           product_profits=product_profits, sale_names=sale_names, sale_profits=sale_profits,
                           dates=dates, sales_per_days=sales_per_days, sale_date=sale_date, daily_profit=daily_profit)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


        new_user = (fname, email, hashed_password)
        check = check_email(email)
        if check == None:
            insert_users(new_user)
            flash('Registered successful login')
            return redirect(url_for('login'))
        else:
            flash('user already exist use a different email')
            return render_template('register.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # check if user is registered
        check = check_email(email)
        if check == None:
            flash('user does not exist register')
            return redirect(url_for('register'))
        else:
            # check if password matches hashed_password
            if bcrypt.check_password_hash(check[-1],password):
                session['email']= email
                flash('login successful')
                return redirect(url_for('dashboard'))
            else:
                flash('wong password or email')
                return render_template('login.html')
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('email')
    flash('you have been logged out')
    return redirect(url_for('login'))


app.run(debug=True)
