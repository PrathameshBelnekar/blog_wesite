from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import requests
import random

application = Flask(__name__)
app = application

app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250) ,nullable=False)
    email = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(250), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

app.secret_key = "prathamesh"




with app.app_context():
    db.create_all()


@app.route('/')
def home():
    response = requests.get("https://newsapi.org/v2/everything?q=apple&from=2023-02-09&to=2023-02-09&sortBy=popularity&apiKey=22e330aeed3646468b056af2559abccd").json()
    data = response["articles"]
    random_num1 = random.randint(0,99)
    random_num2 = random.randint(0,99)
    random_num3 = random.randint(0,99)
    random_num4 = random.randint(0,99)
    random_post1 = data[random_num1]
    random_post2 = data[random_num2]
    random_post3 = data[random_num3]
    random_post4 = data[random_num4]
    return render_template("index.html",posts1 = random_post1,posts2= random_post2,posts3= random_post3,posts4= random_post4)



@app.route('/signup' , methods=["GET", "POST"])
def register():
    if request.method == "POST":

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password= hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("post"))
    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact_data")
def contact_data():
    all_rec = db.session.query(contact).all()
    return render_template("contact_data.html",all_rec = all_rec)

@app.route("/contact_view" ,methods=["GET", "POST"])
def contact_view():
    if request.method == "POST":
        new_contact = contact(
            
            name=request.form["name"],
            email= request.form["email"],
            phone_number=request.form["tel"],
            message = request.form["message"]
        )
        db.session.add(new_contact)
        db.session.commit()
    return render_template("contact_view.html")



@app.route('/logout')
def logout():
    pass


@app.route('/post')
def post():
    return render_template("post.html")


if __name__ == "__main__":
    app.run(debug=True)
