from flask import Flask, redirect, render_template, request, jsonify,url_for
from flask import session
from table import *
from functools import wraps
from model import *
import io
import base64
import plotly.io as pio
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.io import to_image
from flask_caching import Cache
from tmodel import *

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)
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
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect('/dashbord')

@app.route('/dashbord')
@cache.cached(timeout=120)
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

# @app.route('/login')
# def login():
#     if request.method=='GET':
#         return render_template('login.html')
#     else:
#         #add in bd after checking if valid and if does not exist
#         return render_template('/dashbord')

# @app.route('/signup')
# def signup():
#     if request.method=='GET':
#         if 'username' in session:
#             return redirect('/dashbord')
#         else:
#             return render_template('login/singup.html')
#     else:
#         #create this user
#         return render_template('/dashbord')
    
@app.route('/model',methods=["POST","GET"])
@login_required
def calc():
    if request.method=='GET':
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
        return render_template('modelchoose.html',**context)
    else:
        val = request.form['get']
        val = int(val)
        img1,img2 = model4(val)
        # img1_filename = f"static/images/"+str(val)+"1.png"
        # img2_filename = f"static/images/"+str(val)+"2.png"
        # img1_path = os.path.join(os.getcwd(), img1_filename)
        # img2_path = os.path.join(os.getcwd(), img2_filename)
        # img1.write_image(img1_path)
        # img2.write_image(img2_path)
        return render_template('output.html',img11=img1,img21=img2)
        # def image_to_base64(fig):
        #     img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        #     print(3)
        #     return img_base64  
        # img1_base64 = image_to_base64(img1)
        # img2_base64 = image_to_base64(img2)

@app.route('/tmodel',methods=["POST","GET"])
@login_required
def calcmode():
    if request.method=='GET':
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
        return render_template('tmodelchoose.html',**context)
    else:
        val = request.form['get']
        val = int(val)
        img2 = renewable(val)
        val1 = request.form['get1']
        val1 = int(val1)
        img3,img4 = stats(val1)
        img1 = thermal(val)
        return render_template('toutput.html',img11=img1,img21=img2,img31=img3,img41=img4)
    
# @app.route('/dashbord/solution')
# @login_required
# def sol():
#     pass
#     #idhar sirf html rahega 

# @app.route('/dashbord/blogs')
# @login_required
# def blogs():
#     pass


if __name__ == '__main__':
    app.run(debug=True)
