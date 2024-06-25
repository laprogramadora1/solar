from app import db

class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(100))
    estado = db.Column(db.Boolean, default=True)
    external_id = db.Column(db.String(60))

    @property
    def serialize(self):
        return {
            
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'external': self.external_id,
            'estado': 1 if self.estado else 0
        }