from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.recipes_model import Recipes
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
#setting a variable for the =Bcrypt
#to get it to work you need to import Bcrypt
bcrypt = Bcrypt(app)

#TODO go back to you database and drop the schema and add date instead of date_time  on cooke_date
# registration page
@app.route("/")
def show_reg():
    return render_template("index.html")


#registration form 
#validates creation of a user
#encrypts the password
@app.route("/", methods = ["post"])
def create_user():
    #validate the registration
    print(request.form)
    if not User.validate(request.form):
        return redirect("/")
        #encrypt the password
    data = {
        **request.form,
        "password": bcrypt.generate_password_hash(request.form["password"])
    }
    session["id"]= User.add_one(data)
    return redirect("/recipes")


#login form
#checks that the email and the password match in the database  
#checks for the password hash encryptions
#stores the id in session
@app.route("/log_in",methods = ["post"])
def log_in():
    #checks that the email and the password match in the database 
    data = {
        "email": request.form["email"]
    }
    user = User.get_by_email(data)
    if not user:
        flash("Invalid Email/Password","match")
        print("user")
        return redirect("/")
        #checks for the password hash encryptions
    if not bcrypt.check_password_hash(user.password,request.form["password"]):
        flash("Invalid Email/Password","match")
        print("password")
        return redirect("/")
        #stores the id in session
    session["id"]=user.id
    session["f_name"] = user.f_name
    session["l_name"] = user.l_name
    session["email"] = user.email
    return redirect("/recipes")


# renders dashboard page
# redirect to the login page if user try to go to the dashboard using the url
@app.route("/recipes")
def log_in_form():
    # redirect to the login page if user try to go to the dashboard using the url
    if "id" not in session:
        return redirect("/")
    user = User.get_by_id({"id": session["id"]})
    # grab all the recipes
    list_recipes = Recipes.get_all_with_users() 
    return render_template("user_home_page.html",user = user,list_recipes = list_recipes)


#erase session and logs user out
@app.route("/log_out")
def log_out():
    session.pop("id")
    return redirect("/")