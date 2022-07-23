from flask import flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipes_model import Recipes

#always use the decorator
@app.route("/recipes")
def create_recipes():
    if "id" not in session:
        return redirect("/")
    # User.get_by_id({"id": session["id"]})
    return render_template("recipes.html")

@app.route("/recipes/new")
def display_create_recipes():
    if "id" not in session:
        return redirect("/")
    # User.get_by_id({"id": session["id"]})
    return render_template("create_recipes.html")



@app.route("/recipe/create",methods =["post"] )
def create_recipe():
    #validate
    if not Recipes.validate_recipe(request.form):
        return redirect("/recipes/new")
    #create the recipe
    # user = User.get_by_id({"id": session["id"]})
    data = {
        **request.form,
            "user_id":session["id"]
    }
    Recipes.create_recipe(data)
    #redirect to recipe
    return redirect("/recipes")


#renders the show on template and grabs the id
@app.route("/recipes/<int:num>")
def show_one(num):
    if "id" not in session:
        return redirect("/")
    data ={
        "id":num
    }
    current_recipe = Recipes.get_one_with_user(data)
    return render_template("show_one_recipe.html", current_recipe = current_recipe)


@app.route("/recipes/update/<int:num>")
def display_update_recipe(num):
    if "id" not in session:
        return redirect("/")
    data ={
        "id":num
    }
    current_recipe = Recipes.get_one_with_user(data)
    return render_template("update_recipe.html",current_recipe = current_recipe)

@app.route("/recipe/update/<int:num>", methods = ["post"])
def update_recipe(num):
    if not Recipes.validate_recipe(request.form):
        return redirect(f"/recipes/update/{num}")
    recipe_data = {
        **request.form,
        "id":num,
        "user_id":session["id"]
    }
    Recipes.update_one(recipe_data)
    return redirect("/recipes")


@app.route("/recipes/delete/<int:num>")
def delete_one_recipe(num):
    data = {
        "id": num
    }
    Recipes.delete_one(data)
    return redirect("/recipes")