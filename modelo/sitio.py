from app import db
from modelo.censosolar import CensoSolar
import enum
import json
from flask import jsonify

class FuenteEnum(enum.Enum):
    METEONORM = 'METEONORM'
    NASA_SSE = 'NASA_SSE'
    NREL = 'NREL'
    def getValue(self):
        return self.value
    def __json__(self):
        return self.value

class Sitio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    ubicacion = db.Column(db.String(255))
    estado = db.Column(db.Boolean, default=True)
    fuente = db.Column(db.Enum(FuenteEnum))
    external_id = db.Column(db.String(100))
    promedio = db.Column(db.Double, default=0.0)
    irradiacion = db.Column(db.Double, default=0.0)
    #coef_reflexion = db.Column(db.Double, default=0.2)
    longitud = db.Column(db.Double, default=0.0)
    latitud = db.Column(db.Double, default=0.0)
    id_canton = db.Column(db.Integer, db.ForeignKey('canton.id'),nullable=True)

    censosolar = db.relationship('CensoSolar', backref='sitio', lazy=True)
    
    def __init__(self, nombre, estado, external_id, promedio, irradiacion, longitud, latitud, fuente, id_canton, ubicacion):
        self.nombre = nombre
        self.estado = estado
        self.promedio = promedio
        self.irradiacion = irradiacion
        self.external_id = external_id 
        self.fuente = fuente
        self.longitud = longitud
        self.latitud = latitud
        self.id_canton = id_canton
        self.ubicacion = ubicacion
    
    @property
    def serialize_id(self):
       """Return object data in easily serializable format"""
       
       return {
           'external'         : self.external_id,
           'nombre':self.nombre.upper(),
           'ubicacion': self.ubicacion,
           'estado' : self.estado,
           'canton' : self.canton.external_id,
           'provincia' : self.canton.provincia.external_id,
           'irradiacion' : self.irradiacion,
           'promedio' : self.promedio,
           #'coef_reflexion' : self.coef_reflexion,
           'longitud' : self.longitud,
           'latitud' : self.latitud,
           'fuente': self.fuente.getValue()
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    
    @property
    def serialize_nombre(self):
       """Return object data in easily serializable format"""
       
       return {
           'external'         : self.external_id,
           'nombre':self.nombre.upper(),
           'estado' : 'Activo' if self.estado else 'Desactivo',
           'canton' : self.canton.nombre.upper(),
           'provincia' : self.canton.provincia.nombre.upper(),
           'irradiacion' : self.irradiacion,
           'promedio' : self.promedio,
           #'coef_reflexion' : self.coef_reflexion,
           'longitud' : self.longitud,
           'latitud' : self.latitud,
           'ubicacion': self.ubicacion,
           'fuente': self.fuente.getValue()
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    
    @property
    def serialize_only_data(self):
       """Return object data in easily serializable format"""
       
       return {
           'external'         : self.external_id,
           'nombre':self.nombre.upper(),
           'estado' : self.estado,
           'canton' : self.canton.external_id,
           'provincia' : self.canton.provincia.external_id,
           
       }

    def getCanton(id):
        from modelo.canton import Canton
        
        canto = Canton.query.get(id)
        return  jsonify(canto.serialize())
    
    def getListEnum():
        lista = []
        for data in FuenteEnum:
            lista.append({"key":data.name,"value":data.value})            
        return lista
    
    @property
    def guardar(self):
        db.session.add(self)
        db.session.commit()
        return self.id
    
    @property
    def modificar(self):         
        db.session.merge(self)
        db.session.commit()
        return self.id  
