from flask import Flask, request, jsonify, make_response, current_app
from flask_sqlalchemy import SQLAlchemy
import uuid # for public id
import jwt
from datetime import datetime, timedelta
from functools import wraps
from  modelo.cuenta import Cuenta


def token_required(f):
    @wraps(f)
    def decored(*args, **kwargs):
        token = None
        #print("******************* TOKEN ***********")
        #print(request.headers)
        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']
        
        if not token:
            return make_response(        
                jsonify({"msg":"ERROR", "code": 401, "datos":{"error":"Token no existe"}}),
                401
            )
        try:
            
            data = jwt.decode(token, algorithms="HS512", verify=True, key=current_app.config['SECRET_KEY'])
            print(token)
            user = Cuenta.query.filter_by(external_id = data["external"]).first()
            if not user:
                return make_response(        
                    jsonify({"msg":"ERROR", "code": 401, "datos":{"error":"Token invalidado o sesion expirado"}}),
                    401
                )                
        except Exception as error:
            print(error)    
            return make_response(        
                    jsonify({"msg":"ERROR", "code": 401, "datos":{"error":"Token invalidado por expiracion"}}),
                    401
            )
        return f(*args, **kwargs)
    return decored