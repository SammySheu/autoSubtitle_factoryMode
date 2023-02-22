from flask import Blueprint, render_template, request, jsonify
from app.module.db import User, addUser

from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies
)
import datetime

user = Blueprint('user', __name__)

@user.route('/register', methods = ['GET'])
def registerGet():
    return render_template('register_page.html', msg = request.args.get('msg'))

@user.route('/register', methods=['POST'])
def registerPost():
    searchEmail = User.query.filter(User.user_email==request.form['email']).first()
    if not searchEmail:             # if email doesn't exist, build one
        user = User(   
            user_email = request.form['email'],
            user_password = request.form['password'],
        )
        addUser(user)
        return jsonify(msg = 'Register successfully'), 200
    else:
        return jsonify(msg = 'Email already exists'), 200

@user.route('/login', methods=['GET'])
def loginGet():
    return render_template('login_page.html', msg = request.args.get('msg'))

@user.route('/login', methods=['POST'])   
def loginPost():
    searchData = User.query.filter_by(user_email=request.form['user_email']).first()
    if searchData:
        if searchData.user_password == request.form['user_password']:
            # Make a response that put access_token into headers
            response = jsonify({"msg": "login successful"})
            access_token = create_access_token(identity={'user_id':searchData.user_id}, expires_delta=datetime.timedelta(minutes=60))
            set_access_cookies(response, access_token)
            return response
        else:
            return jsonify(msg = 'Incorrect password\n'), 200
    else:
        return jsonify(msg = 'No such user was found\n'), 200
    
@user.route("/logout", methods=["POST"])
def logout_with_cookies():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response