from app import db
from sqlalchemy.sql import func

class Cuenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(150), unique = True)    
    estado = db.Column(db.Boolean, default=True)
    external_id = db.Column(db.String(100))
    clave = db.Column(db.String(250))
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id'),nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    #persona = db.relationship('Persona', backref='cuenta', lazy=True)

    

    def copy(self, value):
        self.clave = value.clave
        self.correo = value.correo
        self.estado = value.estado
        self.external_id = value.external_id
        self.id_persona = value.id_persona
        self.id = value.id
        self.created_at = value.created_at
        self.updated_at = value.updated_at

    @property
    def serialize(self):
        
        return {            
            'correo': self.correo,
            'estado': 1 if self.estado else 0,
            'external': self.external_id
        }
    
    
    def getPersona(self, id_p):
        from modelo.persona import Persona        
        return Persona.query.filter_by(id = id_p).first()
    
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