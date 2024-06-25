from app import db
from datetime import datetime

class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    consumo_mensual = db.Column(db.Double)
    coef_reflexion = db.Column(db.Double)
    tipo_edificio = db.Column(db.String(100))
    inclinacion = db.Column(db.Double)
    orientacion = db.Column(db.Double)
    fuente = db.Column(db.String(100))
    potencia = db.Column(db.Double)
    eficiencia = db.Column(db.Double)
    factor_sombra = db.Column(db.Double)
    rendimiento = db.Column(db.Double)
    demanda_potencia_electronica = db.Column(db.Double)
    costo_instalacion = db.Column(db.Double)    
    estado = db.Column(db.Boolean, default=True)
    external_id = db.Column(db.String(60))
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id'),nullable=False)
    id_sitio = db.Column(db.Integer, db.ForeignKey('sitio.id'),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def serialize(self):
        return {
            
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'external': self.external_id,
            'estado': 1 if self.estado else 0
        }