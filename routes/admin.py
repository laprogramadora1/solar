from flask import Blueprint, jsonify, json, make_response, request
from modelo.provincia import Provincia
from modelo.canton import Canton
from modelo.sitio import Sitio
from modelo.catalogo import Catalogo
from modelo.rol import Rol
from modelo.persona import Persona
from modelo.cuenta import Cuenta
from modelo.censosolar import CensoSolar
from modelo.proyecto import Proyecto
from controllers.personaControl import PersonaControl
from marshmallow import Schema, fields, ValidationError, validate
from util.validate import Trim, not_blank
import uuid
from routes.schema.schema import SitioSchema, SitioEditSchema, CensoSchema, InicioSchema, PersonaPerfilSchema, PersonaGuardarSchema
from controllers.authenticate import token_required

admin = Blueprint('admin', __name__)
#pip install flask-marshmallow
class ProvinciaSchema(Schema):
    nombre = Trim(fields.String(transform='upper'), validate=not_blank, required=True, error_messages={"required": "Se requiere el nombre"})
class ProvinciaEditSchema(ProvinciaSchema):
    external = Trim(fields.String(), validate=not_blank, required=True, error_messages={"required": "Se requiere el external"})
class CantonEditSchema(ProvinciaEditSchema):
    external_canton = Trim(fields.String(), validate=not_blank, required=True, error_messages={"required": "Se requiere el external del canton"})

@admin.route('/api/inicio')
def inicio():
    print("ESTOY EN INICIO")
    pc = PersonaControl()
    pc.crear_roles()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":"OK se ha creado"}
                ),
                200,
            )

@admin.route('/api/sesion', methods =['POST'])
def sesion():
    pc = PersonaControl()
    request_data = request.json    
    print(request)
    schema = InicioSchema()
    try:
        
        result = schema.load(request_data)
        i = pc.inicio_sesion(result)
        if i == -4:
            return make_response(
                jsonify(
                    {"message": "Error", "code": 400, "datos":"Cuenta o clave no son correctas, o cuenta no existe"}
                ),
                400,
            )
        else:
            return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":i}
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
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":"OK se ha creado"}
                ),
                200,
            )

@admin.route('/api/admin/total')
def total():
    provincias = Provincia.query.count()
    canton = Canton.query.count()
    sitios = Sitio.query.count()
    user = Persona.query.count()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":{"prov":provincias,"canton":canton,"sitios":sitios,"user":user}}
                ),
                200,
            )

@admin.route('/api/admin/provincias/activate')
@token_required
def lista_provincia_activate():
    provincias = Provincia.query.filter_by(estado = True).order_by("nombre").all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize for i in provincias])}
                ),
                200,
            )

@admin.route('/api/admin/provincias')
@token_required
def lista_provincia():
    provincias = Provincia.query.order_by("nombre").all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize for i in provincias])}
                ),
                200,
            )

@admin.route('/api/admin/provincias/<external>')
@token_required
def provincia(external):
    provincias = Provincia.query.filter_by(external_id = external).first()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":(provincias.serialize)}
                ),
                200,
            )

@admin.route('/api/admin/provincias/guardar', methods =['POST'])
@token_required
def provincia_guardar():
    
    request_data = request.json    
    print(request)
    schema = ProvinciaSchema()
    try:
        
        result = schema.load(request_data)
        pr = Provincia.query.filter_by(nombre = result.get("nombre")).first()
        if pr:
             return make_response(
                jsonify(
                    {"message": "OK", "code": 406, "datos":"Provincia con nombre repetido"}
                ),
                406,
            )
        else:
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
@token_required
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
@token_required
def lista_sitios():
    sitios = Sitio.query.all()
    #return jsonify(sitios=[i.serialize_id for i in sitios])
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize_nombre for i in sitios])}
                ),
                200,
            )


#CANTONES
@admin.route('/api/admin/canton/activate')
@token_required
def lista_canto_activate():
    provincias = Canton.query.filter_by(estado = True).order_by("nombre").all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize for i in provincias])}
                ),
                200,
            )

@admin.route('/api/admin/canton')
@token_required
def lista_canton():
    provincias = Canton.query.all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize for i in provincias])}
                ),
                200,
            )

@admin.route('/api/admin/canton/<external>')
@token_required
def canton(external):
    provincias = Canton.query.filter_by(external_id = external).first()
    if provincias:
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":(provincias.serialize)}
                ),
                200,
            )
    else:
        return make_response(
                    jsonify(
                        {"message": "Error", "code": 400, "datos":"No existe el canton"}
                    ),
                    400,
                )

@admin.route('/api/admin/canton/provincia/<external>')
@token_required
def canton_provincia(external):
    provincia = Provincia.query.filter_by(external_id = external).first()
    if provincia:
        canton = Canton.query.filter_by(id_provincia = provincia.id).all()
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize for i in canton])}
                ),
                200,
            )
    else:
        return make_response(
                    jsonify(
                        {"message": "Error", "code": 400, "datos":"No existe la provincia"}
                    ),
                    400,
                )

@admin.route('/api/admin/canton/guardar', methods =['POST'])
@token_required
def canto_guardar():    
    request_data = request.json    
    
    schema = ProvinciaEditSchema()
    try:
        
        result = schema.load(request_data)
        
        provincia = Provincia.query.filter_by(external_id = result.get("external")).first()
        if provincia:
            prov = Canton(result.get("nombre"), True, uuid.uuid4(), provincia.id)
            #prov = Provincia(result.get("nombre"), True, uuid.uuid4())
            prov.guardar
            return make_response(
                    jsonify(
                        {"message": "OK", "code": 200, "datos":"Se ha registrado correctamente"}
                    ),
                    200,
                )
        else:
            return make_response(
                    jsonify(
                        {"message": "Error", "code": 400, "datos":"No existe la provincia"}
                    ),
                    400,
                )
    except ValidationError as err:
        return make_response(
                jsonify(
                    {"message": "Error", "code": 400, "datos":(err.messages)}
                ),
                400,
            )
        #return jsonify(err.messages), 400

@admin.route('/api/admin/canton/modificar', methods =['POST'])
@token_required
def canton_modificar():
    
    request_data = request.json    
    print(request)
    schema = CantonEditSchema()
    try:
        result = schema.load(request_data)
        provincia = Provincia.query.filter_by(external_id = result.get("external")).first()
        if provincia:
            
            print(uuid.uuid4())
            prov = Canton.query.filter_by(external_id = result.get("external_canton")).first()#Provincia(result.get("nombre"), True, uuid.uuid4())
            if prov:
                prov.nombre = result.get("nombre")
                prov.id_provincia = provincia.id
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
                            {"message": "Error", "code": 400, "datos":"No existe el canton"}
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


#SITIO-------

@admin.route('/api/admin/sitio/activate')
@token_required
def lista_sitio_activate():
    provincias = Sitio.query.filter_by(estado = True).order_by("nombre").all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize for i in provincias])}
                ),
                200,
            )

@admin.route('/api/admin/sitio')
@token_required
def lista_sitio():
    provincias = Sitio.query.all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize for i in provincias])}
                ),
                200,
            )

@admin.route('/api/admin/sitio/<external>')
@token_required
def sitio(external):
    provincias = Sitio.query.filter_by(external_id = external).first()
    if provincias:
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":(provincias.serialize_id)}
                ),
                200,
            )
    else:
        return make_response(
                    jsonify(
                        {"message": "Error", "code": 400, "datos":"No existe el canton"}
                    ),
                    400,
                )

@admin.route('/api/admin/sitio/nombre/<external>')
@token_required
def sitio_nombre(external):
    provincias = Sitio.query.filter_by(external_id = external).first()
    if provincias:
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":(provincias.serialize_nombre)}
                ),
                200,
            )
    else:
        return make_response(
                    jsonify(
                        {"message": "Error", "code": 400, "datos":"No existe el canton"}
                    ),
                    400,
                )

@admin.route('/api/admin/sitio/canton/<external>')
@token_required
def sitio_canton(external):
    canton = Canton.query.filter_by(external_id = external).first()
    if canton:
        print(canton.id)
        sitios = Sitio.query.filter_by(id_canton = canton.id).all()
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize_nombre for i in sitios])}
                ),
                200,
            )
    else:
        return make_response(
                    jsonify(
                        {"message": "Error", "code": 400, "datos":"No existe la provincia"}
                    ),
                    400,
                )

@admin.route('/api/admin/sitio/guardar', methods =['POST'])
@token_required
def sitio_guardar():    
    request_data = request.json
    
    schema = SitioSchema()
    print(request_data)
    try:        
        result = schema.load(request_data)
        canto = Canton.query.filter_by(external_id = result.get("external_canton")).first()
        if canto:
            #nombre, estado, external_id, promedio, irradiacion, fuente, longitud, latitud, id_canton
            sit = Sitio(result.get("nombre"), True, uuid.uuid4(),float(result.get("promedio")),float(result.get("irradiacion")),float(result.get("longitud")),float(result.get("latitud")), result.get("fuente"), canto.id, result.get("ubicacion"))
            #prov = Provincia(result.get("nombre"), True, uuid.uuid4())
            sit.guardar
            return make_response(
                    jsonify(
                        {"message": "OK", "code": 200, "datos":"Se ha registrado correctamente"}
                    ),
                    200,
                )
        else:
            return make_response(
                    jsonify(
                        {"message": "Error", "code": 400, "datos":"No existe la provincia"}
                    ),
                    400,
                )
    except ValidationError as err:
        return make_response(
                jsonify(
                    {"message": "Error", "code": 400, "datos":(err.messages)}
                ),
                400,
            )
        #return jsonify(err.messages), 400

@admin.route('/api/admin/sitio/modificar', methods =['POST'])
@token_required
def sitio_modificar():
    
    request_data = request.json    
    
    schema = SitioEditSchema()
    try:
        result = schema.load(request_data)
        canto = Canton.query.filter_by(external_id = result.get("external_canton")).first()
        if provincia:
            
            print(uuid.uuid4())
            prov = Sitio.query.filter_by(external_id = result.get("external")).first()#Provincia(result.get("nombre"), True, uuid.uuid4())
            if prov:
                prov.nombre = result.get("nombre")
                prov.id_canton = canto.id
                prov.ubicacion = result.get("ubicacion")
                prov.longitud = float(result.get("longitud"))
                prov.latitud = float(result.get("latitud"))
                prov.promedio = float(result.get("promedio"))
                prov.irradiacion = float(result.get("irradiacion"))
                prov.fuente = result.get("fuente")
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
                            {"message": "Error", "code": 400, "datos":"No existe el canton"}
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
    

#CENSO SOLAR-------


@admin.route('/api/admin/censo')
@token_required
def lista_censo():
    provincias = CensoSolar.query.all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize_nombre for i in provincias])}
                ),
                200,
            )

@admin.route('/api/admin/censo/<external>')
@token_required
def censo(external):
    provincias = CensoSolar.query.filter_by(external_id = external).first()
    if provincias:
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":(provincias.serialize_id)}
                ),
                200,
            )
    else:
        return make_response(
                    jsonify(
                        {"message": "Error", "code": 400, "datos":"No existe el canton"}
                    ),
                    400,
                )

@admin.route('/api/admin/censo/sitio/<external>')
@token_required
def censo_sitio(external):
    sit = Sitio.query.filter_by(external_id = external).first()
    if sit:
        
        censos = CensoSolar.query.filter_by(id_sitio = sit.id).all()
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize_nombre for i in censos])}
                ),
                200,
            )
    else:
        return make_response(
                    jsonify(
                        {"message": "Error", "code": 400, "datos":"No existe la provincia"}
                    ),
                    400,
                )

@admin.route('/api/admin/censo/guardar', methods =['POST'])
@token_required
def censo_guardar():    
    request_data = request.json
    
    schema = CensoSchema()
    print(request_data)
    try:        
        result = schema.load(request_data)
        sit = Sitio.query.filter_by(external_id = result.get("external")).first()
        if sit:
            #nombre, estado, external_id, promedio, irradiacion, fuente, longitud, latitud, id_canton
            censos = CensoSolar.query.filter_by(id_sitio = sit.id).all()
            if len(censos) > 0:
                #modificar
                
                for i in censos:
                    
                    if i.mes.getValue() == "ENERO":
                        i.irradiacion = result.get("enero")
                    if i.mes.getValue() == "FEBRERO":
                        i.irradiacion = result.get("febrero")
                    if i.mes.getValue() == "MARZO":
                        i.irradiacion = result.get("marzo")
                    if i.mes.getValue() == "ABRIL":
                        i.irradiacion = result.get("abril")
                    if i.mes.getValue() == "MAYO":
                        i.irradiacion = result.get("mayo")
                    if i.mes.getValue() == "JUNIO":
                        i.irradiacion = result.get("junio")
                    if i.mes.getValue() == "JULIO":
                        i.irradiacion = result.get("julio")
                    if i.mes.getValue() == "AGOSTO":
                        i.irradiacion = result.get("agosto")
                    if i.mes.getValue() == "SEPTIEMBRE":
                        i.irradiacion = result.get("septiembre")
                    if i.mes.getValue() == "OCTUBRE":
                        i.irradiacion = result.get("octubre")
                    if i.mes.getValue() == "NOVIEMBRE":
                        i.irradiacion = result.get("noviembre")
                    if i.mes.getValue() == "DICIEMBRE":
                        i.irradiacion = result.get("diciembre")

                    i.modificar
                sit.promedio = result.get("promedio")
                sit.modificar
            else:
                #guardar
                censo1 = CensoSolar("ENERO", result.get("enero"), uuid.uuid4(), sit.id)
                censo1.guardar
                censo2 = CensoSolar("FEBRERO", result.get("febero"), uuid.uuid4(), sit.id)
                censo2.guardar
                censo3 = CensoSolar("MARZO", result.get("marzo"), uuid.uuid4(), sit.id)
                censo3.guardar
                censo4 = CensoSolar("ABRIL", result.get("abril"), uuid.uuid4(), sit.id)
                censo4.guardar
                censo5 = CensoSolar("MAYO", result.get("mayo"), uuid.uuid4(), sit.id)
                censo5.guardar
                censo6 = CensoSolar("JUNIO", result.get("junio"), uuid.uuid4(), sit.id)
                censo6.guardar
                censo7 = CensoSolar("JULIO", result.get("julio"), uuid.uuid4(), sit.id)
                censo7.guardar
                censo8 = CensoSolar("AGOSTO", result.get("agosto"), uuid.uuid4(), sit.id)
                censo8.guardar
                censo9 = CensoSolar("SEPTIEMBRE", result.get("septiembre"), uuid.uuid4(), sit.id)
                censo9.guardar
                censo10 = CensoSolar("OCTUBRE", result.get("octubre"), uuid.uuid4(), sit.id)
                censo10.guardar
                censo11 = CensoSolar("NOVIEMBRE", result.get("noviembre"), uuid.uuid4(), sit.id)
                censo11.guardar
                censo12 = CensoSolar("DICIEMBRE", result.get("diciembre"), uuid.uuid4(), sit.id)
                censo12.guardar
                sit.promedio = result.get("promedio")
                sit.modificar
            #(result.get("nombre"), True, uuid.uuid4(),float(result.get("promedio")),float(result.get("irradiacion")),float(result.get("longitud")),float(result.get("latitud")), result.get("fuente"), canto.id, result.get("ubicacion"))
            #prov = Provincia(result.get("nombre"), True, uuid.uuid4())
            #sit.guardar
            return make_response(
                    jsonify(
                        {"message": "OK", "code": 200, "datos":"Se ha registrado correctamente"}
                    ),
                    200,
                )
        else:
            return make_response(
                    jsonify(
                        {"message": "Error", "code": 400, "datos":"No existe la provincia"}
                    ),
                    400,
                )
    except ValidationError as err:
        return make_response(
                jsonify(
                    {"message": "Error", "code": 400, "datos":(err.messages)}
                ),
                400,
            )
        #return jsonify(err.messages), 400

@admin.route('/api/admin/censo/modificar', methods =['POST'])
@token_required
def censo_modificar():    
    request_data = request.json       
    schema = SitioEditSchema()
    try:
        result = schema.load(request_data)
        canto = Canton.query.filter_by(external_id = result.get("external_canton")).first()
        if provincia:    
            
            prov = Sitio.query.filter_by(external_id = result.get("external")).first()#Provincia(result.get("nombre"), True, uuid.uuid4())
            if prov:
                prov.nombre = result.get("nombre")
                prov.id_canton = canto.id
                prov.ubicacion = result.get("ubicacion")
                prov.longitud = float(result.get("longitud"))
                prov.latitud = float(result.get("latitud"))
                prov.promedio = float(result.get("promedio"))
                prov.irradiacion = float(result.get("irradiacion"))
                prov.fuente = result.get("fuente")
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
                            {"message": "Error", "code": 400, "datos":"No existe el canton"}
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

#PERFIL DE USUARIO

@admin.route('/api/admin/perfil/<external>')
@token_required
def perfil(external):
    pc = PersonaControl()
    person = pc.getPerfil(external)
    if person != None:
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":person.serialize_nombre}
                ),
                200,
            )
    else:
        return make_response(
                jsonify(
                    {"message": "OK", "code": 400, "datos":"No existe este perfil"}
                ),
                400,
            )
    
@admin.route('/api/admin/perfil/modificar', methods =['POST'])
@token_required
def perfil_modificar():
    pc = PersonaControl()
    request_data = request.json
    
    schema = PersonaPerfilSchema()
    print(request_data)
    try:        
        result = schema.load(request_data)
        person = pc.modificar_perfil(result)
        if person ==  -1:
            return make_response(
                    jsonify(
                        {"message": "OK", "code": 400, "datos":"No existe este perfil"}
                ),
                400,
            )
        elif person == -2:
            return make_response(
                    jsonify(
                        {"message": "OK", "code": 400, "datos":"No existe este perfil"}
                ),
                400,
            )
        else:
            return make_response(
                    jsonify(
                        {"message": "OK", "code": 200, "datos":"Se ha modificado exitosamente, por favor reinicie sesión"}
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
    
@admin.route('/api/admin/persona/lista')
@token_required
def lista_persona():
    provincias = Persona.query.all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize_data for i in provincias])}
                ),
                200,
            )

@admin.route('/api/admin/persona/guardar', methods =['POST'])
@token_required
def persona_guardar():
    pc = PersonaControl()
    request_data = request.json
    
    schema = PersonaGuardarSchema()

    try:        
        result = schema.load(request_data)
        person = pc.guardar_user(result)
        if person ==  -1:
            return make_response(
                    jsonify(
                        {"message": "OK", "code": 400, "datos":"No existe este perfil"}
                ),
                400,
            )
        elif person == -2:
            return make_response(
                    jsonify(
                        {"message": "OK", "code": 400, "datos":"Ni existe ese permiso"}
                ),
                400,
            )
        else:
            return make_response(
                    jsonify(
                        {"message": "OK", "code": 200, "datos":"Se ha modificado exitosamente, por favor reinicie sesión"}
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
@admin.route('/api/admin/persona/estado/<external>')
@token_required
def persona_estado(external):
    pc = PersonaControl()
    person = pc.cambiar_estado(external)
    if person != -1:
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":"Estado actualizado correctamente"}
                ),
                200,
            )
    else:
        return make_response(
                jsonify(
                    {"message": "OK", "code": 400, "datos":"No existe este usuario"}
                ),
                400,
            )
