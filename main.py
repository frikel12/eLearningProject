from flask import render_template, url_for, request, redirect, session, Flask
# from flask import Blueprint
# from flask_paginate import Pagination, get_page_parameter
import MySQLdb.cursors
import re
import MySQLdb

app = Flask(__name__)

app.secret_key='youssefrikel12'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/account')
def account():
    return render_template('account.html')


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'jobsdb',
}


def connect_to_database():
    return MySQLdb.connect(**db_config)


def close_database_connection(connection, cursor):
    cursor.close()
    connection.close()


# 404 error code handler
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)





