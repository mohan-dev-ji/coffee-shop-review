from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField, SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm
class CreatePostForm(FlaskForm):
    name = StringField("Name of Coffee Shop", validators=[DataRequired()])
    map_url = StringField("Google Maps - Share - Embed", validators=[DataRequired()])
    img_url = StringField("img location", validators=[DataRequired()])
    location = StringField("Address", validators=[DataRequired()])
    has_sockets = RadioField("Plug Sockets", choices = ['Yes', 'No'])
    has_toilet = RadioField("Toilet", choices = ['Yes', 'No'])
    has_wifi = RadioField("WiFi", choices = ['Yes', 'No'])
    # can_take_calls = RadioField("Landline", choices = ['Yes', 'No'])
    seats = SelectField("Seats", choices = ['0-10', '11-20', '21-30', '31-40', '41-50', '50+'])
    coffee_price = StringField("Coffe Price", validators=[DataRequired()])
    opening_hours = StringField("Opening Hours", validators=[DataRequired()])
    # date = StringField("Date of Post", validators=[DataRequired()])
    review_para_1 = CKEditorField("Paragraph 1", validators=[DataRequired()])
    review_img_1 = StringField("Image 1", validators=[DataRequired()])
    review_para_2 = CKEditorField("Paragraph 2", validators=[DataRequired()])
    review_img_2 = StringField("Image 2", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


# Create a form to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


# Create a form to add comments
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    star_rating = SelectField('Rating', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], coerce=int, validators=[DataRequired()])
    submit = SubmitField("Submit Comment")
