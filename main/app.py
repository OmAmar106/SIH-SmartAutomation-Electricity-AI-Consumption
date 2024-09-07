from flask import Flask, redirect, render_template, request, jsonify,url_for
from flask import session
from table import *
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
db.init_app(app)
app.app_context().push()
app.secret_key = "APtlnuRu04uv"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            # Redirect to login if 'username' is not in session
            return redirect(url_for('login',next=request.url))
        return f(*args, **kwargs)
    return decorated_function
  
@app.route('/')
def main():
    if 'username' in session:
        return redirect('/dashbord')
    else:
        return redirect('/login')

@app.route('/login')
def login():
    if request.method=='GET':
        if 'username' in session:
            return redirect('/dashbord')
        else:
            return render_template('login/login.html')
    else:
        #after saving the inputs here
        return render_template('/dashbord')

@app.route('/signup')
def signup():
    if request.method=='GET':
        if 'username' in session:
            return redirect('/dashbord')
        else:
            return render_template('login/singup.html')
    else:
        #create this user
        return render_template('/dashbord')
    
@app.route('/dashbord')
@login_required
def dashbord():
    return render_template('user/dashbord.html')

@app.route('/dashbord/calculate')
@login_required
def calc():
    #idhar model import krne ke bad , usse output leke webpage par dikhana hain :) 
    #ek bar create hua toh fir directly show kr denge ya toh save kr lenge backend main

@app.route('/dashbord/solution')
@login_required
def sol():
    #idhar sirf html rahega 

@app.route('/dashbord/blogs')
@login_required
def blogs():

@app.route('/profile/<string:s>')
@login_required
def profile(s):

if __name__ == '__main__':
    app.run(debug=True)