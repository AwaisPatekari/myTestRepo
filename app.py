from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
app.secret_key = 'super secret key'

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html',session = True,name = session['username'])
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    articles = mongo.db.articles
    existing_articles = articles.find({})
    return render_template('articles.html',articles=existing_articles)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email' : request.form['email']})
        #existing_user_password = users.find_one({'password' : request.form['password']})
        if existing_user['email'] == request.form['email'] and existing_user['password'] == request.form['password']:
            session['username'] = existing_user['name']
            return redirect(url_for('index'))
        return "This profile does not exist!"
    return render_template('login.html')

@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email' : request.form['email']})
        if existing_user is None:
            users.insert({'name': request.form['username'], 'email' : request.form['email'], 'password': request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return "That email already exists!"
    return render_template('signup.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return render_template('index.html')


if  __name__ == '__main__':
    app.run(debug=True)
