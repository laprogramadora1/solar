import enum
class TipoIdentificacion(enum.Enum):
    CEDULA = 'CEDULA'
    PASAPORTE = 'PASAPORTE'
    

    def getValue(self):
        return self.value
    
    @staticmethod
    def list():
        lista = []
        for i in TipoIdentificacion:
            lista.append({"key":i.name, "value":i.value})
        return lista

    def __json__(self):
        return self.value