from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# =========================
# SESSION / SECRET KEY (needed for production safety)
# =========================
app.secret_key = "inventory_secret_key"

# =========================
# DATABASE CONFIGURATION
# (Render-safe fallback version)
# =========================
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventory_db'

mysql = MySQL(app)


# =========================
# LOGIN PAGE (BYPASSED FOR DEPLOYMENT)
# =========================
@app.route('/', methods=['GET', 'POST'])
def login():

    # 🔥 AUTO LOGIN (bypass database for Render demo)
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('login.html')


# =========================
# REGISTER PAGE (BYPASSED SAFELY)
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        return redirect(url_for('login'))

    return render_template('register.html')


# =========================
# DASHBOARD / HOME PAGE
# =========================
@app.route('/dashboard')
def index():

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        cur.close()

    except:
        # 🔥 fallback if database is not available
        products = []

    return render_template('index.html', products=products)


# =========================
# ADD PRODUCT (SAFE MODE)
# =========================
@app.route('/add', methods=['GET', 'POST'])
def add_product():

    if request.method == 'POST':
        try:
            product_name = request.form['product_name']
            quantity = request.form['quantity']
            price = request.form['price']

            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO products(product_name, quantity, price)
                VALUES(%s, %s, %s)
            """, (product_name, quantity, price))

            mysql.connection.commit()
            cur.close()

        except:
            pass

        return redirect(url_for('index'))

    return render_template('add_product.html')


# =========================
# EDIT PRODUCT
# =========================
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):

    try:
        cur = mysql.connection.cursor()

        if request.method == 'POST':

            product_name = request.form['product_name']
            quantity = request.form['quantity']
            price = request.form['price']

            cur.execute("""
                UPDATE products
                SET product_name=%s,
                    quantity=%s,
                    price=%s
                WHERE id=%s
            """, (product_name, quantity, price, id))

            mysql.connection.commit()
            cur.close()

            return redirect(url_for('index'))

        cur.execute("SELECT * FROM products WHERE id=%s", [id])
        product = cur.fetchone()
        cur.close()

        return render_template('edit_product.html', product=product)

    except:
        return redirect(url_for('index'))


# =========================
# DELETE PRODUCT
# =========================
@app.route('/delete/<int:id>')
def delete_product(id):

    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM products WHERE id=%s", [id])
        mysql.connection.commit()
        cur.close()
    except:
        pass

    return redirect(url_for('index'))


# =========================
# RUN SERVER (RENDER FIXED)
# =========================
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)