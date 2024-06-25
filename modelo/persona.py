from app import db
from modelo.tipoIdentificacion import TipoIdentificacion
#from sqlalchemy.sql import func
from datetime import datetime
from modelo.cuenta import Cuenta
class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(15))
    nombres = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    tipo = db.Column(db.Enum(TipoIdentificacion))
    external_id = db.Column(db.String(60))
    
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id'),nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    cuenta = db.relationship('Cuenta', backref='persona', lazy=True)

    @property
    def _apellido(self):
        return self.apellidos
    @_apellido.setter
    def _apellido(self, value):
        self.apellidos = value
    
    def copy(self, value):
        self.id = value.id
        self.dni = value.dni
        self.apellidos = value.apellidos
        self.nombres = value.nombres
        self.external_id = value.external_id
        self.tipo = value.tipo
        
        self.created_at = value.created_at
        self.updated_at = value.updated_at
        self.id_rol = value.id_rol
        

    @property
    def serialize(self):       
        return {
            
            'dni': self.dni,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'external': self.external_id,
	   
            'estado': self.estado.getValue(),
            'cuenta': [i.serialize for i in self.cuenta]
        }
