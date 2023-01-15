from datetime import datetime
from app import db,login_manager
from . import main
from .forms import UserForm,NamerForm,LoginForm,ItemsForm,OrderForm,AddToCartForm,PaymentForm
from ..models import Users,Items,Products,Cart
from flask import Flask, render_template,flash,request,redirect,url_for,session,current_app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from binance.client import Client




@main.route('/')
def index():
    return render_template("base_home.html")

@main.route('/menu_base')
def menu_base():
    products = Products.query.all()
    return render_template("menu_base.html",products=products)

@main.route('/user/<name>')
def user(name):
    return render_template("user.html",user_name=name)



@main.route('/login',methods=['GET','POST']) #post method needed for page containing forms
def login():
    form = LoginForm()
    #validating form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            # checking the hash
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Login Successful!")
                return redirect(url_for('main.dashboard'))
                
            else:
                flash("Wrong password -- Try again")
                return render_template("login.html",form=form)
        else:
            flash("That user doesn't exist -- Try again")
            return render_template("login.html",form=form)
    else:
        return render_template("login.html",form=form)

@main.route('/dashboard', methods=["GET","POST"])
@login_required
def dashboard():
    return render_template("dashboard.html", active_nav='dashboard')

@main.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    flash("You are logged out!")
    return render_template("index.html")



@main.route('/add-item', methods = ['POST','GET'])
@login_required
def add_item():
    form = ItemsForm(request.form)
    if form.validate_on_submit():
        item = Items(name=form.name.data, size = form.size.data, price = form.price.data)
        db.session.add(item)
        db.session.commit()
        flash("Item added successfully")
        return redirect(url_for('main.add_item'))
    else:
        return render_template("add_item.html", form=form)
        
        
   
@main.route('/items')
@login_required
def view_items():
    items = Items.query.order_by(Items.id)
    return render_template("items.html",items=items)

@main.route('/item/<int:id>')
@login_required
def item_zoom(id):
    form = ItemsForm()
    item = Items.query.get_or_404(id)
    return render_template('item.html', item=item,form=form)


@main.route('/item/delete/<int:id>')
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
            return render_template("items.html",items=items)

        
        
        except:
            flash("There was a problem deleting item..try again")
            items = Items.query.order_by(Items.id)
            return render_template("items.html",items=items)

    else:
         flash("Unauthorized Access")
         items = Items.query.order_by(Items.date_posted)
         return render_template("items.html",items=items)



@main.route('/item/edit/<int:id>', methods = ["GET","POST"])
@login_required
def edit_item(id):
    item = Items.query.get_or_404(id)
    form = ItemsForm()
    if form.validate_on_submit():
        item.name = form.name.data
       # post.author = form.author.data
        item.size = form.size.data
        item.price = form.price.data
        db.session.add(item)
        db.session.commit()
        flash("Item has been updated!")
        return redirect(url_for('main.item',id=item.id))
    
    if current_user.id == 1:
        form.name.data = item.name
    # form.author.data = post.author
        form.size.data = item.size
        form.price.data = item.price
        return render_template('edit_item.html', form=form)

    else:
        flash("Unauthorized Access")
        items = Items.query.order_by(Items.date_posted)
        return render_template("items.html",items=items)




@main.route('/user/add', methods =['GET','POST'])
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

#update database
@main.route('/update/<int:id>', methods =['GET','POST'])
@login_required
def update(id):
    form = UserForm()
    # Query the database to retrieve the existing user row
    user = Users.query.get(id)
    form.name.data = user.name
    form.email.data = user.email

    # If the form is being submitted
    if request.method == 'POST':

        # Modify the values of the retrieved user object
        user.name = request.form['name']
        user.email = request.form['email']

        # Hash the new password
        hashed_password = generate_password_hash(request.form['password_hash'], "sha256")
        user.password_hash = hashed_password

        # Commit the changes to the database
        db.session.commit()

        # Redirect to the dashboard page
        return redirect(url_for('main.dashboard'))

    # If the form is being displayed
    else:
        # Render the update template
        return render_template('update.html', user=user, form=form)

@main.route('/delete/<int:id>', methods =['GET','POST'])
@login_required
def delete(id):
    user = db.session.query(Users).get(id)
    form = UserForm(request.form)
    if request.method == "GET":
        db.session.delete(user)
        db.session.commit()
        flash("User Deleted Sucessfully")
        return render_template("add_user.html",form=form,user=user)
    
    else:
        return render_template("add_user.html",form=form,user=user)



@main.route('/menu')
@login_required
def menu():
    products = Products.query.all()
    return render_template('menu.html', products=products)


@main.route('/menu/<string:category>', methods=['GET','POST'])
@login_required
def menu_category(category):
    items = Items.query.filter_by(category=category).all()
    cart = [] 
    if request.method == 'POST':
        # get the item name and size from the request form
        item_name = request.form.get('item_name')
        item_size = request.form.get('item_size')

        # find the item in the list of items
        for item in items:
            if item.name == item_name and item.size == item_size:
                # add the item to the cart
                cart = request.form.get('cart', [])
                cart.append(item)

        # render the template with the updated cart
        return render_template('menu_category.html', items=items, cart=cart)


    return render_template("menu_category.html", items=items,cart=cart)

@main.route('/menu_base/<string:category>', methods=['GET','POST'])
def menu_category_base(category):
    items = Items.query.filter_by(category=category).all()
    return render_template("menu_category_base.html", items=items)
    

@main.route('/add_to_cart/<int:id>', methods=['GET', 'POST'])
def add_to_cart(id):
    form = AddToCartForm()
    item = Items.query.get(id)
    items = Items.query.all()
    form.name.choices = [item.name]
    
    if form.validate_on_submit():
        # Add the product to the cart and redirect to the cart page
        item_id = form.name.data
        quantity = form.quantity.data

        # Check if the item is already in the cart
        existing_item = Cart.query.filter_by(item_id=item_id, user_id=current_user.id).first()

        # If the item is already in the cart, update the quantity
        if existing_item:
            existing_item.quantity += quantity
        # If the item is not in the cart, add it as a new entry
        else:
            new_item = Cart(user_id=current_user.id, item_id=item_id, quantity=quantity)
            db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('main.view_cart'))
    return render_template('add_to_cart.html', form=form, items=items, item = item)


def calculate_total(cart_items, total):
        # Iterate over the items in the cart and calculate the total
        for item in cart_items:
            # Get the item from the Items table using the item_id in the Cart item
            item_obj = Items.query.filter_by(id=item.item_id).first()
            if item_obj:
                total += item_obj.price * item.quantity
                total += item_obj.price * item.quantity
        return total


@main.route('/cart')
def view_cart():
    # Get all the items in the cart for the current user
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = 0

    total = calculate_total(cart_items, total=total)

    # Create a list of dictionaries that contain the name, price, and total
    # for each item in the cart
    cart_items_with_attributes = []
    for item in cart_items:
        item_obj = Items.query.filter_by(id=item.item_id).first()
        if item_obj:
            item_dict = {
                'name': item_obj.name,
                'price': item_obj.price,
                'quantity': item.quantity,
                'total': item_obj.price * item.quantity
            }
            cart_items_with_attributes.append(item_dict)

    return render_template('cart.html', cart=cart_items_with_attributes, total=total, active_nav='cart')


@main.route('/clear-cart')
def clear_cart():
  # Get all the items in the cart for the current user
  cart_items = Cart.query.filter_by(user_id=current_user.id).all()
  
  # Delete all the items in the cart
  for item in cart_items:
    db.session.delete(item)
  db.session.commit()
  
  return redirect(url_for('main.view_cart'))




@main.route("/checkout", methods=['GET','POST'])
def checkout():
    # Render the checkout page template
    return render_template("checkout.html")









