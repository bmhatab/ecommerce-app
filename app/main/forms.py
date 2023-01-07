from .. import main
from flask import Flask, render_template,flash,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import Form,StringField,SubmitField,PasswordField,SelectField,IntegerField
from wtforms.validators import DataRequired,EqualTo,Length
from wtforms.widgets import TextArea



class NamerForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Name : ", validators=[DataRequired()])
    email = StringField("Email : ", validators=[DataRequired()])
    submit = SubmitField("Submit")
    password_hash = PasswordField("Password : ", validators=[DataRequired(),EqualTo('password_hash_v',message="Passwords must match!")])
    password_hash_v = PasswordField("Confirm Password : ", validators=[DataRequired()])

    
class ItemsForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    size = StringField("Size", validators=[DataRequired()], widget=TextArea())
    price = StringField("Price", validators=[DataRequired()])
    submit = SubmitField()



class OrderForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    size = StringField("Size", validators=[DataRequired()], widget=TextArea())
    quantity = StringField("Quantity", validators=[DataRequired()])
    submit = SubmitField()


class ProductsForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()], widget=TextArea())
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField()

class AddToCartForm(FlaskForm):
    name = SelectField('Name', validators=[DataRequired()], choices=[])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add to Cart')