from app import db

from modelo.sitio import Sitio
from flask import jsonify

class Catalogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    estado = db.Column(db.Boolean, default=True)
    external_id = db.Column(db.String(100))
    valor = db.Column(db.String(100))
    id_padre = db.Column(db.Integer)

    def __init__(self, nombre, estado, external_id, valor, id_padre):
        self.nombre = nombre
        self.estado = estado
        self.external_id = external_id
        self.valor = valor
        self.id_padre = id_padre
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       
       return {
           'external'         : self.external_id,
           'nombre':self.nombre,
           'estado' : self.estado,
           'valor':self.valor,
           'ref':self.id_padre
           
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
           'valor' : self.valor,
           'ref': self.id_padre
           
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    
    