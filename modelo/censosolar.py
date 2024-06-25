from app import db
import enum
#from modelo.provincia import Provincia
from flask import jsonify
#from sqlalchemy import Enum

class MesesEnum(enum.Enum):
    ENERO = 1
    FEBRERO = 2
    MARZO = 3
    ABRIL = 4
    MAYO = 5
    JUNIO = 6
    JULIO = 7
    AGOSTO = 8
    SEPTIEMBRE = 9
    OCTUBRE = 10
    NOVIEMBRE = 11
    DICIEMBRE = 12


    

class CensoSolar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.Enum(MesesEnum))
    irradiacion = db.Column(db.Double, default=0.0)
    
    external_id = db.Column(db.String(100))
    id_sitio = db.Column(db.Integer, db.ForeignKey('sitio.id'),nullable=False)
    

    def __init__(self, mes, irradiacion, external_id, promedio):
        self.mes = mes
        self.irradiacion = irradiacion
        self.external_id = external_id 
        
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       
       return {
           'external'         : self.external_id,
           'mes':self.mes,
          
           'irradiacion' : self.irradiacion
           
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    
    @property
    def serialize_id(self):
       """Return object data in easily serializable format"""
       
       return {
           'external'         : self.external_id,
           'mes':self.mes,
           'irradiacion' : self.irradiacion,
           
           'sitio' : self.id_sitio
           
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    
 