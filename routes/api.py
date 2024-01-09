from flask import Blueprint
from modelo.provincia import Provincia
from modelo.canton import Canton
from modelo.sitio import Sitio
from modelo.catalogo import Catalogo
from flask import jsonify, json, make_response, request
from util.calculos import Calculos
from decimal import Decimal
from flask_cors import CORS
api = Blueprint('api', __name__)


CORS(api)
cors = CORS(api, resource={
    r"/*":{
        "origins":"*"
    }
})
@api.route('/')
def home():
    return 'Hola api solar'
#provincias
@api.route('/api/provincia')
def lista_provincias():
    provincias = Provincia.query.all()
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize for i in provincias])}
                ),
                200,
            )
    #return jsonify(provincias=[i.serialize for i in provincias])


#cantones
@api.route('/api/canton')
def lista_cantones():
    #cantones = Canton.query.all()
    cantones = Canton.query.filter(Canton.provincia.has())
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize_id for i in cantones])}
                ),
                200,
            )
#Lista los cantones por provinvia
@api.route('/api/canton/<provinciaE>')
def lista_cantones_provincia(provinciaE):
    prov = Provincia.query.filter_by(external_id=provinciaE).first()
    if(prov):

        cantones = Canton.query.filter_by(id_provincia=prov.id).all()
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize_id for i in cantones])}
                ),
                200,
            )
    else:
       return make_response(
                jsonify(
                    {"message": "Error la provincia no existe", "code": 200, "datos":[]}
                ),
                200,
            ) 
    #return jsonify(cantones=[i.serialize_id for i in cantones])



#Lista los sitios por canton
@api.route('/api/sitio/canton/<externalC>')
def lista_sitios_canton(externalC):
    canton = Canton.query.filter_by(external_id=externalC).first()
    if(canton):

        sitios = Sitio.query.filter_by(id_canton=canton.id).all()
        #return jsonify(sitios=[i.serialize_id for i in sitios])
        return make_response(
                    jsonify(
                        {"message": "OK", "code": 200, "datos":([i.serialize_id for i in sitios])}
                    ),
                    200,
        )
    else:
        return make_response(
                jsonify(
                    {"message": "Error, el canton no existe", "code": 200, "datos":[]}
                ),
                200,
            )

#Lista los sitios por canton y fuente
@api.route('/api/sitio/canton/<externalC>/<fuente>')
def lista_sitios_canton_fuente(externalC, fuente):
    canton = Canton.query.filter_by(external_id=externalC).first()
    if(canton):

        sitios = Sitio.query.filter_by(id_canton=canton.id, fuente=fuente).all()
        #return jsonify(sitios=[i.serialize_id for i in sitios])
        return make_response(
                    jsonify(
                        {"message": "OK", "code": 200, "datos":([i.serialize_id for i in sitios])}
                    ),
                    200,
        )
    else:
        return make_response(
                jsonify(
                    {"message": "Error, el canton no existe", "code": 200, "datos":[]}
                ),
                200,
            )

#Fuentes
@api.route('/api/fuentes')
def lista_fuentes():
    sitios = Sitio.getListEnum()
    #return jsonify(sitios=[i.serialize_id for i in sitios])
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":sitios}
                ),
                200,
            )

#sitios
@api.route('/api/catalogo/edificio')
def lista_catalogo_edificio():
    catalogo = Catalogo.query.filter_by(nombre = 'tipo_edificio').first()
    if(catalogo):

        edificio = Catalogo.query.filter_by(id_padre = 14).all()
        #return jsonify(sitios=[i.serialize_id for i in sitios])
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize_id for i in edificio])}
                ),
                200,
            )
    else:
        return make_response(
                jsonify(
                    {"message": "Error, el catalogo edificio no existe", "code": 200, "datos":[]}
                ),
                200,
            )
#sitios
@api.route('/api/sitio')
def lista_sitios():
    sitios = Sitio.query.all()
    #return jsonify(sitios=[i.serialize_id for i in sitios])
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize_id for i in sitios])}
                ),
                200,
            )
#Sitio por external
@api.route('/api/sitio/obtener/<external>')
def obtener_sitio(external):
    sitio = Sitio.query.filter_by(external_id=external).first()
    if(sitio):
        
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":sitio.serialize_id}
                ),
                200,
            )
    else:
        return make_response(
                jsonify(
                    {"message": "Error, el canton no existe", "code": 200, "datos":[]}
                ),
                200,
            )
    #objCalc = Calculos()
    #calculos = objCalc.calculos_datos(sitio.latitud, sitio.coef_reflexion, sitio.inclinacion, sitio.orientacion)
    
    
#<coef_reflexion>/<inclinacion>/<orientacion>/<external>/<potencia>/<eficiencia>/<fs>/<rendimiento>
@api.route('/api/calculos', methods =['POST'])
def calcular_post():
    data = request.json
    consumo_mensual = data.get('consumo_mensual')
    tipo_edificio = data.get('tipo_edificio')
    coef_reflexion = data.get('coef_reflexion')
    inclinacion = data.get('inclinacion')
    orientacion = data.get('orientacion')
    external = data.get('external')
    potencia = data.get('potencia')
    eficiencia = data.get('eficiencia')
    fs = data.get('fs')
    rendimiento = data.get('rendimiento')
    demanda_potencia_electronica = data.get('demanda_potencia_electronica')
    costo_instalacion = data.get('costo_instalacion')

    objCalc = Calculos()
    sitio = Sitio.query.filter_by(external_id=external).first()
    if(sitio):
        #print (sitio)
        calculos = objCalc.calculos_datos(float(costo_instalacion), float(demanda_potencia_electronica), float(consumo_mensual), tipo_edificio, sitio.latitud, float(coef_reflexion), float(inclinacion), float(orientacion), sitio, float(potencia), float(eficiencia), float(fs), float(rendimiento))    
        #return jsonify(calculos)
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":calculos}
                ),
                200,
            )
    else:
        return make_response(
                jsonify(
                    {"message": "No se encuentra el sitio", "code": 403}
                ),
                403,
            )
    
