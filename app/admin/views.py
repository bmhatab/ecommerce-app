from datetime import datetime
from flask import Flask, render_template,flash,request,redirect,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from app.admin import admin
from app.models import Items,Users,Products
from app import db
from flask_wtf import FlaskForm
from wtforms import Form,StringField,SubmitField,PasswordField,ValidationError
from wtforms.validators import DataRequired,EqualTo,Length
from wtforms.widgets import TextArea



class ItemsForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    size = StringField("Size", validators=[DataRequired()], widget=TextArea())
    price = StringField("Price", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    submit = SubmitField()

class UserForm(FlaskForm):
    name = StringField("Name : ", validators=[DataRequired()])
    email = StringField("Email : ", validators=[DataRequired()])
    submit = SubmitField("Submit")
    password_hash = PasswordField("Password : ", validators=[DataRequired(),EqualTo('password_hash_v',message="Passwords must match!")])
    password_hash_v = PasswordField("Confirm Password : ", validators=[DataRequired()])

class ProductsForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()], widget=TextArea())
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField()



@admin.route('/')
def index():
    return render_template("admin_index.html")

@admin.route('/add-item', methods = ['POST','GET'])
@login_required
def add_item():
    form = ItemsForm(request.form)
    if form.validate_on_submit():
        item = Items(name=form.name.data, size = form.size.data, price = form.price.data, category=form.category.data)
        db.session.add(item)
        db.session.commit()
        flash("Item added successfully")
        return redirect(url_for('admin.add_item'))
    else:
        return render_template("admin/add_item.html", form=form)
        
        
   
@admin.route('/items')
@login_required
def view_items():
    items = Items.query.order_by(Items.id)
    return render_template("admin/items.html",items=items)

@admin.route('/item/<int:id>')
@login_required
def item_zoom(id):
    item = Items.query.get_or_404(id)
    return render_template('admin/item.html', item=item)


@admin.route('/item/delete/<int:id>')
@login_required
def delete_item(id):
    item_to_delete = Items.query.get_or_404(id)
    id = current_user.id
    if id == 1:
        try:
            db.session.delete(item_to_delete)
            db.session.commit()
            flash("Item was deleted")
            items = Items.query.order_by(Items.date_posted)
            return render_template("admin/items.html",items=items)

        
        
        except:
            flash("There was a problem deleting item..try again")
            items = Items.query.order_by(Items.id)
            return render_template("admin/items.html",items=items)

    else:
         flash("Unauthorized Access")
         items = Items.query.order_by(Items.date_posted)
         return render_template("admin/items.html",items=items)



@admin.route('/item/edit/<int:id>', methods = ["GET","POST"])
@login_required
def edit_item(id):
    item = Items.query.get_or_404(id)
    form = ItemsForm()
    if form.validate_on_submit():
        item.name = form.name.data
       # post.author = form.author.data
        item.size = form.size.data
        item.price = form.price.data
        item.category = form.category.data
        #db.session.add(item)
        db.session.commit()
        flash("Item has been updated!")
        return redirect(url_for('admin.edit_item',id=item.id))
    
    if current_user.id == 1:
        form.name.data = item.name
    # form.author.data = post.author
        form.size.data = item.size
        form.price.data = item.price
        return render_template('admin/edit_item.html', form=form)

    else:
        flash("Unauthorized Access")
        items = Items.query.order_by(Items.date_posted)
        return render_template("admin/items.html",items=items)




@admin.route('/user/add', methods =['GET','POST'])
def add_user(): 
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash password first
            hash_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data,email=form.email.data,password_hash=hash_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        flash("User Added Sucessfully")
    #To display user names on the page 
    our_users = Users.query.order_by(Users.date_added)   
    return render_template('add_user.html',form=form,name=name,our_users=our_users)


@admin.route('/add-product', methods = ['POST','GET'])
@login_required
def add_product():
    form = ProductsForm(request.form)
    if form.validate_on_submit():
        product = Products(name=form.name.data, category=form.category.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully")
        return redirect(url_for('admin.add_product'))
    else:
        return render_template("admin/add_product.html", form=form)


@admin.route('/products')
@login_required
def view_products():
    products = Products.query.order_by(Products.id)
    return render_template("admin/products.html",products=products)        

@admin.route('/product/edit/<int:id>', methods = ["GET","POST"])
@login_required
def edit_product(id):
    product = Products.query.get_or_404(id)
    form = ProductsForm()
    if form.validate_on_submit():
        product.name = form.name.data
       # post.author = form.author.data
        product.category = form.category.data
        product.description = form.description.data
        db.session.add(product)
        db.session.commit()
        flash("Product has been updated!")
        #return redirect(url_for('admin.products',id=product.id))
        return render_template('admin/products.html')
    
    if current_user.id == 1:
        form.name.data = product.name
    # form.author.data = post.author
        form.category.data = product.category
        form.description.data = product.description
        return render_template('admin/edit_product.html', form=form)

    else:
        flash("Unauthorized Access")
        product = Products.query.order_by(Products.id)
        return render_template("admin/products.html",product=product)

@admin.route('/product/delete/<int:id>')
@login_required
def delete_product(id):
    product_to_delete = Products.query.get_or_404(id)
    id = current_user.id
    if id == 1:
        try:
            db.session.delete(product_to_delete)
            db.session.commit()
            flash("Product was deleted")
            products = Products.query.order_by(Products.id)
            return render_template("admin/products.html",products=products)

        
        
        except:
            flash("There was a problem deleting item..try again")
            products = Products.query.order_by(Products.id)
            return render_template("admin/products.html",products=products)

    else:
         flash("Unauthorized Access")
         products = Products.query.order_by(Products.id)
         return render_template("admin/products.html",products=products)

