from unittest import result
from flask_app.config.connect_tosql import connectToMySQL
from flask import flash
from flask_app import db 
from flask_app.models.user_model import User

#TODO go back to you database and drop the schema and add date instead of date_time  on cooke_date
class Recipes:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instruction = data["instruction"]
        self.cooked_date = data["cooked_date"]
        self.under_30 = data["under_30"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

#creates recipe
    @classmethod
    def create_recipe(cls,data):
        query = "insert into recipes (name,description,instruction,cooked_date,under_30,user_id) values(%(name)s,%(description)s,%(instruction)s,%(cooked_date)s,%(under_30)s,%(user_id)s);"
        result = connectToMySQL(db).query_db(query,data)
        print(result)
        return result

#joins the 2 tables to get the info from both
    @classmethod
    def get_all_with_users(cls):
        query = "select* from recipes join users on recipes.user_id = users.id;"
        result = connectToMySQL(db).query_db(query)
        #creating a new attribute for the user table the we are importing 
        list_recipes =[]
        for row in result:
            current_recipe = cls(row)
            user_data = {
                **row,
                "id": row["users.id"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            current_user = User(user_data)
            current_recipe.user =current_user
            list_recipes.append(current_recipe)
        return list_recipes


#joining the to tables and getting the the info by the id
    @classmethod
    def get_one_with_user(cls,data):
        query = "select* from recipes join users on recipes.user_id = users.id where recipes.id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        # see if the selected user has a recipe and if so it grabs it 
        if len(result) > 0 :
            current_recipe = cls (result[0])
            #creating a new attribute for the user table the we are importing 
            user_data = {
                **result[0],
                "id": result[0]["users.id"],
                "created_at": result[0]["users.created_at"],
                "updated_at": result[0]["users.updated_at"]
            }
            current_recipe.user = User(user_data)
            return current_recipe
        else:
            return None


    @classmethod
    def update_one(cls,data):
        query = "update recipes set name = %(name)s, description =%(description)s, instruction = %(instruction)s,cooked_date = %(cooked_date)s,under_30 = %(under_30)s where id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        return result



    @classmethod
    def delete_one(cls,data):
        query = "delete from recipes where id = %(id)s;"
        result =  connectToMySQL(db).query_db(query,data)
        return result

#validations
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        # for name
        if len(recipe["name"]) == 0:
            flash("you must add a name","r_name")
            is_valid = False
        elif len(recipe["name"]) < 3:
            flash("name must be at least 3 character")
            is_valid = False
            #for c
        if len(recipe["description"]) == 0:
            flash("you must add a description","r_description")
            is_valid = False
        elif len(recipe["description"]) < 3:
            flash("description must be at least 3 character","r_description")
            is_valid = False
            #for instruction
        if len(recipe["instruction"]) == 0:
            flash("you must add an instruction","r_instruction")
            is_valid = False
        elif len(recipe["instruction"]) < 3:
            flash("instructions must be at least 3 character","r_instruction")
            is_valid = False
            #for cooked_date
        if  len(recipe["cooked_date"]) == 0:
            flash("you must add a cooked date","r_cooked_date")
            is_valid = False
        #for under_30
        if recipe["under_30"] =="":
            flash("you must say if this recipe is under 30 minutes or not","under_30")
            is_valid = False
        return is_valid
