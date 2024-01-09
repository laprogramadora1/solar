from app import db

from modelo.canton import Canton

class Provincia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    estado = db.Column(db.Boolean, default=True)
    external_id = db.Column(db.String(100))
    cantones = db.relationship('Canton', backref='provincia', lazy=True)

    def __init__(self, nombre, estado, external_id):
        self.nombre = nombre
        self.estado = estado
        self.external_id = external_id 
    
    
    def getNombre(self):
        return self.nombre
    
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