from flask import Blueprint
from modelo.provincia import Provincia
from modelo.canton import Canton
from modelo.sitio import Sitio
from modelo.catalogo import Catalogo
from modelo.censosolar import CensoSolar
from flask import jsonify, json, make_response, request
from util.calculos import Calculos
from util.calculosNoSitio import CalculosNoSitio
from decimal import Decimal

from sqlalchemy.orm import load_only
import base64
api = Blueprint('api', __name__)



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

@api.route('/api/sitio/soloCanton/<externalC>')
def lista_sitios_solo_canton(externalC):
    canton = Canton.query.filter_by(external_id=externalC).first()
    if(canton):
        fields = ['nombre']
        sitios = Sitio.query.filter_by(id_canton=canton.id).group_by('nombre').all()
        #return jsonify(sitios=[i.serialize_id for i in sitios])
        return make_response(
                    jsonify(
                        {"message": "OK", "code": 200, "datos":([i.serialize_only_data for i in sitios])}
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

@api.route('/api/sitio/censo/<externalC>/<fuente>')
def lista_sitios_fuente(externalC, fuente):
    sitio = Sitio.query.filter_by(external_id=externalC, fuente=fuente).first()
    
    if(sitio):
        
        censos = CensoSolar.query.filter_by(id_sitio=sitio.id).all()
        #return jsonify(sitios=[i.serialize_id for i in sitios])
        return make_response(
                    jsonify(
                        {"message": "OK", "code": 200, "datos":([i.serialize_nombre for i in censos])}
                    ),
                    200,
        )
    else:
        return make_response(
                jsonify(
                    {"message": "Error, el sitio no existe", "code": 200, "datos":[]}
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

@api.route('/api/meses')
def lista_meses():
    sitios = CensoSolar.getListEnum()
    #return jsonify(sitios=[i.serialize_id for i in sitios])
    return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":sitios}
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
    fuente = data.get('fuente')
    external = data.get('external')#es el sitio pero aqui hay q buscar 
    external_64 = base64.b64decode(external).decode('UTF-8')
    #xcv = str(external_64,encoding='utf-8')
    print(tipo_edificio)
    potencia = data.get('potencia')
    eficiencia = data.get('eficiencia')
    fs = data.get('fs')
    rendimiento = data.get('rendimiento')
    demanda_potencia_electronica = data.get('demanda_potencia_electronica')
    costo_instalacion = data.get('costo_instalacion')
    separate_external = external_64.split(";")
    #print(separate_external[0])
    if len(separate_external) >= 2:

        objCalc = Calculos()
        canton = Canton.query.filter_by(external_id = separate_external[1]).first()
        if canton:
            sitio = Sitio.query.filter_by(nombre=separate_external[0]).filter_by(id_canton = canton.id).filter_by(fuente = fuente).first()
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
                            {"message": "No se encuentra el sitio*", "code": 403}
                        ),
                        403,
                    )
        else:
                return make_response(
                        jsonify(
                            {"message": "No se encuentra el canton", "code": 403}
                        ),
                        403,
                    )
    else:
            return make_response(
                    jsonify(
                        {"message": "No se encuentra el sitio", "code": 403}
                    ),
                    403,
                )


@api.route('/api/calculos/sinsitio', methods =['POST'])
def calcular_sin_sitio_post():
    data = request.json
    consumo_mensual = data.get('consumo_mensual')
    tipo_edificio = data.get('tipo_edificio')
    coef_reflexion = data.get('coef_reflexion')
    inclinacion = data.get('inclinacion')
    orientacion = data.get('orientacion')
    fuente = data.get('fuente')
    #external = data.get('external')#es el sitio pero aqui hay q buscar 
    #external_64 = base64.b64decode(external).decode('UTF-8')
    #xcv = str(external_64,encoding='utf-8')
    print(tipo_edificio)
    potencia = data.get('potencia')
    eficiencia = data.get('eficiencia')
    fs = data.get('fs')
    rendimiento = data.get('rendimiento')
    demanda_potencia_electronica = data.get('demanda_potencia_electronica')
    costo_instalacion = data.get('costo_instalacion')
    #separate_external = external_64.split(";")
    #print(separate_external[0])
    meses = data.get('meses') 
    if len(meses) == 13:
        objCalc = CalculosNoSitio()        
        censos = []
        for key in meses:
            c1 = CensoSolar(key.upper(), float(meses[key]),"",0)            
            censos.append(c1)
            print(c1.mes+"  "+str(c1.irradiacion))
        
        calculos = objCalc.calculos_datos_sin_sitio(float(costo_instalacion), float(demanda_potencia_electronica), float(consumo_mensual), tipo_edificio, float(data.get('lat')), float(coef_reflexion), float(inclinacion), float(orientacion), censos, float(potencia), float(eficiencia), float(fs), float(rendimiento))                
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


#catalogo
@api.route('/api/catalogo/tarifa')
def lista_catalogo_tarifa():
    catalogo = Catalogo.query.filter_by(nombre = 'tarifa').first()
    if(catalogo):
        edificio = Catalogo.query.filter_by(id_padre = catalogo.id).all()        
        return make_response(
                jsonify(
                    {"message": "OK", "code": 200, "datos":([i.serialize_id for i in edificio])}
                ),
                200,
            )
    else:
        return make_response(
                jsonify(
                    {"message": "Error, el catalogo tarifa no existe", "code": 200, "datos":[]}
                ),
                200,
            )

@api.route('/api/catalogo/tarifa/<external>')
def lista_catalogo_edificio(external):
    catalogo = Catalogo.query.filter_by(external_id = external).first()
    if(catalogo):

        edificio = Catalogo.query.filter_by(id_padre = catalogo.id).all()
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