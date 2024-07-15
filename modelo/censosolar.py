from app import db
import enum
#from modelo.provincia import Provincia
from flask import jsonify
#from sqlalchemy import Enum

class MesesEnum(enum.Enum):
    ENERO = 'ENERO'
    FEBRERO = 'FEBRERO'
    MARZO = 'MARZO'
    ABRIL = 'ABRIL'
    MAYO = 'MAYO'
    JUNIO = 'JUNIO'
    JULIO = 'JULIO'
    AGOSTO = 'AGOSTO'
    SEPTIEMBRE = 'SEPTIEMBRE'
    OCTUBRE = 'OCTUBRE'
    NOVIEMBRE = 'NOVIEMBRE'
    DICIEMBRE = 'DICIEMBRE'
    def getValue(self):
        return self.value
    def __json__(self):
        return self.value

    

class CensoSolar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.Enum(MesesEnum))
    irradiacion = db.Column(db.Double, default=0.0)
    
    external_id = db.Column(db.String(100))
    id_sitio = db.Column(db.Integer, db.ForeignKey('sitio.id'),nullable=False)
    

    def __init__(self, mes, irradiacion, external_id, id_sitio):
        self.mes = mes
        self.irradiacion = irradiacion
        self.external_id = external_id 
        self.id_sitio = id_sitio
    
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
    
    @property
    def serialize_nombre(self):
       """Return object data in easily serializable format"""       
       return {
           'external'         : self.external_id,
           'mes':self.mes.getValue(),
           'irradiacion' : self.irradiacion,           
           'sitio' : self.sitio.nombre
           
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    
    def getListEnum():
        lista = []
        for data in MesesEnum:
            lista.append({"key":data.name,"value":data.value})            
        return lista
    
    def getSitio(id):
        from modelo.sitio import Sitio
        
        canto = Sitio.query.get(id)
        return  jsonify(canto.serialize_nombre())
    
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