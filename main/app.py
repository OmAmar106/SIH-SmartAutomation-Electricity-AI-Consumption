from flask import Flask, redirect, render_template, request, jsonify,url_for
from flask import session
from table import *
from functools import wraps
from model import *

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
  
@app.route('/dashbord')
@login_required
def main():
    current_month_peak,current_month_forecast,avg_temp_today = model3()
    current_month = datetime.now().strftime("%b")
    today = datetime.now()
    date = today.strftime("%d %b %y")
    context = {
        "cur_peak" :f"{current_month_peak['yhat']:.2f} MWH",
        "cur_forec" : f"{current_month_forecast['yhat']:.2f} MWH",
        "avg_temp" : f"{avg_temp_today:.2f}",
        "month" : current_month,
        "date" : date
    }
    return render_template('index.html',**context)

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
    
@app.route('/dashbord/model')
@login_required
def calc():
    pass
    #idhar model import krne ke bad , usse output leke webpage par dikhana hain :) 
    #ek bar create hua toh fir directly show kr denge ya toh save kr lenge backend main

@app.route('/dashbord/solution')
@login_required
def sol():
    pass
    #idhar sirf html rahega 

@app.route('/dashbord/blogs')
@login_required
def blogs():
    pass


if __name__ == '__main__':
    app.run(debug=True)