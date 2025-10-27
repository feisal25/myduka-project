# import psycopg2 package
import psycopg2

# connect to the postgress database
connect = psycopg2.connect(
    host='localhost',
    user='postgres',
    dbname='myduka_dp',
    port=5432,
    password='feitorey12'
)
#  declare cursor to perform database operations
curr = connect.cursor()

#  database operations
# def fetch_products():
#     curr.execute('select * from products;')
#     data=curr.fetchall()
#     return data
# product=fetch_products()
# # print(product)

# insert products
# fetch data
def fetch_data(table):
    query = f'select * from {table}'
    curr.execute(query)
    data = curr.fetchall()
    return data


# products = fetch_data('products')
# print(products)
# stock = fetch_data('stock')
# print(stock)
# sales = fetch_data('sales')
# print(sales)



def insert_products(product_values):
    query = "insert into products (name, buying_price, selling_price) VALUES (%s, %s, %s);"
    curr.execute(query, product_values)
    connect.commit()


# new_products = ('papers', 50, 80)
# insert_products(new_products)
# products = fetch_data('products')
# print(products)


# # display sales
# def fetch_sales():
#     curr.execute('select * from sales;')
#     sales=curr.fetchall()
#     return sales



# insert sales
def insert_sales(sales_values):
    query = "insert into sales (pid, quantity, created_at)VALUES (%s, %s, now());"
    curr.execute(query, sales_values)
    connect.commit()


# new_sale= (3, 12,)
# insert_sales(new_sale)
# sales = fetch_data('sales')
# print(sales)


# display stock
# def fetch_stock():
#     curr.execute('select * from stock;')
#     stock=curr.fetchall()
#     return stock

# stock1=fetch_stock()
# print(stock1)

# insert stock
def insert_stock(stock_values):
    query = "insert into stock (pid, stock_quantity)values(%s, %s)"
    curr.execute(query, stock_values)
    connect.commit()


# new_stock=(3,23)
# insert_stock(new_stock)
# stock=fetch_data('stock')



def product_profit():
    query="select products.name as p_name ,sum((products.selling_price - products.buying_price) * sales.quantity) as profit from" \
    " sales join products on sales.pid = products.id group by(p_name);"
    curr.execute(query)
    profit=curr.fetchall()
    return profit

# myprofits=product_profit()
# print(f'my products profits are:{myprofits}')
    


def sales_per_product():
    querry="select products.name as p_name, sum(sales.quantity * products.selling_price) as total_sales from " \
    "products join sales on products.id = sales.pid group by(p_name);"
    curr.execute(querry)
    sales=curr.fetchall()
    return sales

# mysales=sales_per_product()
# print(f'my total sales are:{mysales}')


        # QUERRIES

#  
    # select products.name as p_name ,sum((products.selling_price - products.buying_price) * sales.quantity) as profit from
    # sales join products on sales.pid = products.id group by(p_name);
    
#        
        # select products.name as p_name, sum(sales.quantity * products.selling_price) as total_sales
        # from products join sales on products.id = sales.pid group by(p_name);
   


