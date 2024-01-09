from app import db

from modelo.sitio import Sitio
from flask import jsonify

class Canton(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    estado = db.Column(db.Boolean, default=True)
    external_id = db.Column(db.String(100))
    id_provincia = db.Column(db.Integer, db.ForeignKey('provincia.id'),nullable=False)
    #provincia = db.relationship('Provincia',  primaryjoin='Provincia.id==Canton.id_provincia', remote_side='Provincia.id', uselist=False)
    sitios = db.relationship('Sitio', backref='canton', lazy=True)

    def __init__(self, nombre, estado, external_id):
        self.nombre = nombre
        self.estado = estado
        self.external_id = external_id 
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       
       return {
           'external'         : self.external_id,
           'nombre':self.nombre,
           'estado' : self.estado
           
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    
    @property
    def serialize_id(self):
       """Return object data in easily serializable format"""
       
       return {
           'external'         : self.external_id,
           'nombre':self.nombre,
           'estado' : self.estado,
           'provincia' : self.provincia.external_id
           
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    
    def getProvincia(id):
        from modelo.provincia import Provincia
        
        prov = Provincia.query.get(id)
        return  jsonify(prov.serialize())