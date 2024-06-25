from flask import Blueprint, jsonify, json, make_response, request
from modelo.provincia import Provincia
from modelo.canton import Canton
from modelo.sitio import Sitio
from modelo.catalogo import Catalogo
from modelo.rol import Rol
from modelo.persona import Persona
from modelo.cuenta import Cuenta
from modelo.proyecto import Proyecto

from marshmallow import Schema, fields, ValidationError, validate
from util.validate import Trim, not_blank
import uuid
from flask_cors import CORS
admin = Blueprint('admin', __name__)
#pip install flask-marshmallow




class ProvinciaSchema(Schema):
    nombre = Trim(fields.String(transform='upper'), validate=not_blank, required=True, error_messages={"required": "Se requiere el nombre"})
class ProvinciaEditSchema(ProvinciaSchema):
    external = Trim(fields.String(), validate=not_blank, required=True, error_messages={"required": "Se requiere el nombre"})
    
@admin.route('/api/admin/total')
def total():
    provincias = Provincia.query.count()
    canton = Canton.query.count()
    sitios = len(Sitio.query.group_by("id_canton").all())
    user = Persona.query.count()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":{"prov":provincias,"canton":canton,"sitios":sitios,"user":user}}
                ),
                200,
            )

@admin.route('/api/admin/provincias')
def lista_provincia():
    provincias = Provincia.query.all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize for i in provincias])}
                ),
                200,
            )

@admin.route('/api/admin/provincias/<external>')
def provincia(external):
    provincias = Provincia.query.filter_by(external_id = external).first()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":(provincias.serialize)}
                ),
                200,
            )

@admin.route('/api/admin/provincias/guardar', methods =['POST'])
def provincia_guardar():
    
    request_data = request.json    
    print(request)
    schema = ProvinciaSchema()
    try:
        
        result = schema.load(request_data)
        print(uuid.uuid4())
        prov = Provincia(result.get("nombre"), True, uuid.uuid4())
        prov.guardar
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":"Se ha registrado correctamente"}
                ),
                200,
            )
    except ValidationError as err:
        return make_response(
                jsonify(
                    {"message": "Error", "code": 400, "datos":(err.messages)}
                ),
                400,
            )
        #return jsonify(err.messages), 400

@admin.route('/api/admin/provincias/modificar', methods =['POST'])
def provincia_modificar():
    
    request_data = request.json    
    print(request)
    schema = ProvinciaEditSchema()
    try:
        
        result = schema.load(request_data)
        print(uuid.uuid4())
        prov = Provincia.query.filter_by(external_id = result.get("external")).first()#Provincia(result.get("nombre"), True, uuid.uuid4())
        if prov:
            prov.nombre = result.get("nombre")
            prov.modificar
            return make_response(
                    jsonify(
                        {"message": "OK", "code": 200, "datos":"Se ha editado correctamente"}
                    ),
                    200,
                )
        else:
            return make_response(
                    jsonify(
                        {"message": "Error", "code": 400, "datos":"No existe la provincia"}
                    ),
                    200,
                )
    except ValidationError as err:
        return make_response(
                jsonify(
                    {"message": "Error", "code": 400, "datos":(err.messages)}
                ),
                400,
            )

#sitios
@admin.route('/api/admin/sitio')
def lista_sitios():
    sitios = Sitio.query.all()
    #return jsonify(sitios=[i.serialize_id for i in sitios])
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize_nombre for i in sitios])}
                ),
                200,
            )