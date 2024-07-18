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

    def __init__(self, nombre, estado, external_id, id_provincia):
        self.nombre = nombre
        self.estado = estado
        self.external_id = external_id 
        self.id_provincia = id_provincia
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       
       return {
           'external'         : self.external_id,
           'nombre':self.nombre.upper(),
           'estado' : 'Activo' if self.estado else 'Desactivo',
           'provincia' : self.provincia.external_id,
           'prov': self.provincia.nombre
           
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    
    @property
    def serialize_id(self):
       """Return object data in easily serializable format"""
       
       return {
           'external'         : self.external_id,
           'nombre':self.nombre.upper(),
           'estado' : 'Activo' if self.estado else 'Desactivo',
           'provincia' : self.provincia.external_id,
           'prov': self.provincia.nombre.upper()
           
           #'modified_at': dump_datetime(self.modified_at),
           # This is an example how to deal with Many2Many relations
           #'many2many'  : self.serialize_many2many
       }
    
    def getProvincia(id):
        from modelo.provincia import Provincia
        
        prov = Provincia.query.get(id)
        return  jsonify(prov.serialize())
    
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
