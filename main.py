from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
import os


# import sqlite3
# db = sqlite3.connect("posts.db")

#posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)

# app.config['CKEDITOR_PKG_TYPE'] = "basic"
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)


##CONNECT TO DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("What Kind of Blessing", validators=[DataRequired()])
    subtitle = StringField("Location", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    #img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    #img_url = StringField("Blog Image URL")
    # Notice body's StringField changed to CKEditorField
    body = CKEditorField("Testimony", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=True)


#db.create_all()

# new_post = BlogPost(title="Hurray", subtitle="Hello",date=datetime.now(),
#                     body="Congratulation", author="Kehinde", img_url="")
# db.session.add(new_post)
# db.session.commit()

#all_posts = db.session.query(BlogPost).all()


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post)


# @app.route("/new-post", methods=["GET", "POST"])
# def add_new_post():
#     form = CreatePostForm()
#     return render_template("make-post.html", form=form)

@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            # img_url=form.img_url.data,
            img_url="https://unsplash.com/photos/18N4okmWccM",
            author=form.author.data,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)

@app.route("/edit_post")
def edit_post():
    pass


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


if __name__ == "__main__":
    app.run(debug=True)