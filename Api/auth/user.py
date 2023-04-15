from flask_restx import Namespace, fields, abort, Resource
from ..models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask import request
from datetime import timedelta
from ..utils import db
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jti, jwt_required, unset_jwt_cookies

auth_namespace=Namespace("auth", description="authentication and authorization of a user to be able to create a Note")

signup_model = auth_namespace.model(
    "Signup", {
        "id":fields.String(required=True, description="a user's id"),
        "firstname":fields.String(required=True, description="a user's firstname"),
        "lastname":fields.String(required=True, description="a user's lastname"),
        "email":fields.String(required=True, description="a user's email"),
        "password_hash":fields.String(required=True, description="a user's password")
    }
)

login_model = auth_namespace.model(
    "Login", {
        "id":fields.String(required=True, description="a user's id"),
        "email":fields.String(required=True, description="a user's email"),
        "password_hash":fields.String(required=True, description="a user's password")
    }
)

@auth_namespace.route("/signup")
class Signup(Resource):
    @auth_namespace.doc(description="Signup a user", summary="Signup a new user and add and commit the user into the database")
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(signup_model)
    def post(self):
        data=request.get_json()
        user=User.query.filter_by(email=data.get("email")).first()

        if user:
            abort(409, message="User with that details already exist")

        
        new_user=User(firstname=data.get("firstname"),
                      lastname=data.get("lastname"),
                      email=data.get("email"),
                      password_hash=generate_password_hash(data.get("password_hash")))

        new_user.save()

        return {"message": "Successfully created a new user" }, HTTPStatus.CREATED
    
@auth_namespace.route("/login")
class Login(Resource):
    @auth_namespace.doc(description="Login a user", summary="Login an already existing user who gets an access token and a refresh token")
    @auth_namespace.expect(login_model)
    def post(self):
        data=request.get_json()
        user =User.query.filter_by(email=data.get("email")).first()
        password=check_password_hash(user.password_hash, data.get("password_hash"))

        if not user:
            abort(HTTPStatus.FORBIDDEN, message="User does not exist")

        if user and password:
            access_token=create_access_token(identity=user.firstname)
            refresh_token=create_refresh_token(identity=user.firstname)

            response = {
                "Access token":access_token,
                "refresh_token":refresh_token
            }

            return response, HTTPStatus.OK
        
        else:
            abort(404, message="Invalid user or password")


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @auth_namespace.doc(description="Refresh an access token", summary="Refresh an access token using a refresh token")
    @jwt_required(refresh=True)
    def post(self):
        current_user=get_jwt_identity

        new_token=create_access_token(current_user, expires_delta=timedelta(minutes=30))
        return {"access_token": new_token}, HTTPStatus.OK
        

    

@auth_namespace.route("/logout")
class Logout(Resource):
    @auth_namespace.doc(description="Logout a user", summary="Logout a registered user out of his account")
    @jwt_required()
    def post(self):

        unset_jwt_cookies
        db.session.commit()

        return {"message": "User has been successfully logged out"}, HTTPStatus.OK



            

