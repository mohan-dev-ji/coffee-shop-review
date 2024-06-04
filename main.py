from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CONFIGURE TABLE
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[int] = mapped_column(Integer, nullable=False)
    has_toilet: Mapped[int] = mapped_column(Integer, nullable=False)
    has_wifi: Mapped[int] = mapped_column(Integer, nullable=False)
    can_take_calls: Mapped[int] = mapped_column(Integer, nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=False)
    


with app.app_context():
    db.create_all()


# WTForm
class CreatePostForm(FlaskForm):
    name = StringField("Name of Coffee Shop", validators=[DataRequired()])
    map_url = StringField("Google Maps - Share - Embed", validators=[DataRequired()])
    img_url = StringField("img location", validators=[DataRequired()])
    location = StringField("Address", validators=[DataRequired()])
    has_sockets = RadioField("Plug Sockets", choices = ['Yes', 'No'])
    has_toilet = RadioField("Toilet", choices = ['Yes', 'No'])
    has_wifi = RadioField("WiFi", choices = ['Yes', 'No'])
    can_take_calls = RadioField("Landline", choices = ['Yes', 'No'])
    seats = SelectField("Seats", choices = ['0-10', '11-20', '21-30', '31-40', '41-50', '50+'])
    coffee_price = StringField("Coffe Price", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

@app.route('/login', methods=["GET", "POST"])
def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     password = form.password.data
    #     result = db.session.execute(db.select(User).where(User.email == form.email.data))
    #     # Note, email in db is unique so will only have one result.
    #     user = result.scalar()
    #     # Email doesn't exist
    #     if not user:
    #         flash("That email does not exist, please try again.")
    #         return redirect(url_for('login'))
    #     # Password incorrect
    #     elif not check_password_hash(user.password, password):
    #         flash('Password incorrect, please try again.')
    #         return redirect(url_for('login'))
    #     else:
    #         login_user(user)
    #         return redirect(url_for('get_all_posts'))
    return render_template("login.html")
    # return render_template("login.html", form=form, current_user=current_user)


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(Cafe))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = db.get_or_404(Cafe, post_id)
    print(requested_post.has_sockets)
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        # has_sockets=form.has_sockets.data
        # if has_sockets == "Yes":
        #     has_sockets = 1
        # else:
        #     has_sockets = 0
        new_post = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
            # date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        print(form.has_sockets.data)
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(Cafe, post_id)
    edit_form = CreatePostForm(
        name=post.name,
        map_url=post.map_url,
        img_url=post.img_url,
        location=post.location,
        has_sockets=post.has_sockets,
        has_toilet=post.has_toilet,
        has_wifi=post.has_wifi,
        can_take_calls=post.can_take_calls,
        seats=post.seats,
        coffee_price=post.coffee_price,
    )
    if edit_form.validate_on_submit():
        post.name = edit_form.name.data
        post.map_url = edit_form.map_url.data
        post.img_url = edit_form.img_url.data
        post.location = edit_form.location.data
        post.has_sockets = edit_form.has_sockets.data
        post.has_toilet = edit_form.has_toilet.data
        post.has_wifi = edit_form.has_wifi.data
        post.can_take_calls = edit_form.can_take_calls.data
        post.seats = edit_form.seats.data
        post.coffee_price = edit_form.coffee_price.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = db.get_or_404(Cafe, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


# Code from previous day
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
