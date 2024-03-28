from flask import render_template, url_for, request, redirect, session, Flask
# from flask import Blueprint
# from flask_paginate import Pagination, get_page_parameter
import MySQLdb.cursors
import re
import MySQLdb
import ast


app = Flask(__name__)

app.secret_key='youssefrikel12'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'elearning',
}


def connect_to_database():
    return MySQLdb.connect(**db_config)


def close_database_connection(connection, cursor):
    cursor.close()
    connection.close()


@app.route('/')
def index():
    connection = connect_to_database()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"SELECT * FROM formations ORDER BY nombre_avis DESC LIMIT 3")
    data = cursor.fetchall()

    for i in range(3):
        string = data[i]["idFormateur"]
        result_list = ast.literal_eval(string)[0]
        cursor.execute(f"SELECT * FROM formateur WHERE idFormateur=%s", (result_list,))
        formateur = cursor.fetchone()
        if formateur:
            data[i]['idFormateur'] = formateur["formateur"]
        else:
            data[i]['idFormateur'] = ""

    close_database_connection(connection, cursor)

    return render_template('index.html', data=data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = connect_to_database()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM client WHERE email = %s AND password = %s', (email, password,))
        user = cursor.fetchone()

        close_database_connection(connection, cursor)

        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['email'] = user['email']
            return redirect(url_for('index'))
        else:
            msg = 'Incorrect email / password!'

    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        confirmpass = request.form['confirmpass']

        connection = connect_to_database()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM client WHERE email = %s', (email,))
        account = cursor.fetchone()

        if not email or not password or not nom or not prenom:
            msg = 'Remplir tous les champs!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Adresse email non valide!'
        elif password != confirmpass:
            msg = 'les deux mots de pass ne sont pas identiques'
        elif account:
            msg = 'Compte déjà existant!'
        else:
            cursor.execute('INSERT INTO client(nom, prenom, email, password) VALUES (%s, %s, %s, %s)',
                           (nom, prenom, email, password))
            connection.commit()
            msg = 'INSCRIPTION REUSSI'
            close_database_connection(connection, cursor)
            return redirect(url_for('index'))

    return render_template('register.html', msg=msg)


@app.route('/account', methods=['GET', 'POST'])
def account():
    msg = ''
    if request.method == 'POST':
        old_pass = request.form['old_password']
        new_pass = request.form['new_password']
        confirm_pass = request.form['confirm_new_password']

        connection = connect_to_database()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM client WHERE id = %s', (session['id'],))
        account = cursor.fetchone()

        if not old_pass or not new_pass or not confirm_pass:
            msg = 'Remplir tous les champs!'
        elif old_pass != account["password"]:
            msg = "password actuel n'est pas correct"
        elif new_pass != confirm_pass:
            msg = 'les deux mots de pass ne sont pas identiques'
        else:
            cursor.execute('UPDATE client SET password=%s WHERE id=%s', (new_pass, account['id']))
            connection.commit()
            msg = 'Modification Reussi'
            close_database_connection(connection, cursor)

    return render_template('account.html', msg=msg)


@app.route('/favoris')
def favoris():
    return render_template('favoris.html')


@app.route('/courses')
def courses():
    return render_template('courses.html')


# 404 error code handler
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)





