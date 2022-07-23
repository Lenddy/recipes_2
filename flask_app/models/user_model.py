from flask import flash
from flask_app.config.connect_tosql import connectToMySQL
from flask_app import db
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex =re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')




class User:
    def __init__(self,data):
        self.id = data["id"]
        self.f_name = data["f_name"]
        self.l_name = data["l_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

#adds on user when they create a account
    @classmethod 
    def add_one(cls,data):
        query = "insert into users (f_name,l_name,email,password) values(%(f_name)s,%(l_name)s,%(email)s,%(password)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result


#gets information from the database to validate latter on
    @classmethod 
    def get_by_email(cls,data):
        query = "select * from users where email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
#checks if there is a email that has the same name that the user input 
        if not result:
            return False
        return cls(result[0])


#gets info by id
    @classmethod 
    def get_by_id(cls,data):
        query = "select * from users where id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])


# for validating  info that the user inputs
    @staticmethod
    def validate(user):
        is_valid = True
        if len(user["f_name"]) == 0 :
            flash("a name must be given","f_name")
            is_valid = False
        elif len(user["f_name"]) < 2:
            flash("name must be at lest 2 character long","f_name")
            is_valid = False
        if len(user["l_name"]) == 0:
            flash( "a last name must be given","l_name" )
            is_valid = False
        elif len(user["l_name"]) < 2:
            flash("last name must be at lest 2 character long","l_name")
            is_valid = False
        if len(user["email"]) == 0:
            flash("an email must be given","email")
            is_valid = False
        elif not email_regex.match(user["email"]): 
            flash("email does not follows the right format","email")
            is_valid = False
#checks if their is a email with the same name
        elif User.get_by_email({"email":user["email"]}):
            flash("email is already in use","email")
            is_valid = False
        if len(user["password"]) == 0 :
            flash("a password must be given " ,"password")
            is_valid = False
        elif len(user["password"]) < 8 :
            flash("password must be at lest 8 characters","password")
            is_valid = False
        elif not password_regex.match(user["password"]):
            flash("password must be minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character","password")
            is_valid = False
        elif user["password"] != user["confirm_password"]:
            flash("password does not match","confirm")
            is_valid = False
        return is_valid


