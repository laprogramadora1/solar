from modelo.persona import Persona
from modelo.rol import Rol
from modelo.cuenta import Cuenta
from modelo.tipoIdentificacion import TipoIdentificacion
import uuid
from app import db
import jwt
from datetime import datetime, timedelta
from flask import  current_app
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph
import base64
class PersonaControl:    
    def obtener(self, id):
        return Persona.query.get(id)

    def listar(self):
        return Persona.query.all()    
    
    
    def buscar_external(self, external):
        return Persona.query.filter_by(external_id = external).first()
    
    def guardar(self, data):
        #print(data["apellidos"])
        persona = Persona()
        rol = Rol.query.filter_by(nombre = 'ADMIN').first()
        if rol:
            cuenta = Cuenta.query.filter_by(correo = data["correo"]).first()
            if cuenta:
                return -2    
            else:
                #Persona
                persona.apellidos = data["apellidos"]
                persona.nombres = data["nombres"]                
                persona.external_id = uuid.uuid4()
                persona.dni = data["dni"]
                persona.tipo = "CEDULA"
                persona.id_rol = rol.id
                persona.guardar
                #cuenta
                cuenta_new = Cuenta()
                cuenta_new.correo = data["correo"]
                cuenta_new.clave = genph(data["clave"])
                cuenta_new.external_id = uuid.uuid4()
                cuenta_new.id_persona = persona.id
                cuenta_new.guardar
                return cuenta_new.id
        else:
            return -1
    
    def guardar_user(self, data):
        #print(data["apellidos"])
        persona = Persona()
        rol = Rol.query.filter_by(nombre = 'USER').first()
        if rol:
            cuenta = Cuenta.query.filter_by(correo = data["correo"]).first()
            if cuenta:
                return -2    
            else:
                #Persona
                persona.apellidos = data["apellidos"]
                persona.nombres = data["nombres"]                
                persona.external_id = uuid.uuid4()
                persona.dni = data["dni"]
                persona.tipo = "CEDULA"
                persona.id_rol = rol.id
                persona.guardar
                #cuenta
                cuenta_new = Cuenta()
                cuenta_new.correo = data["correo"]
                cuenta_new.clave = genph(data["clave"])
                cuenta_new.external_id = uuid.uuid4()
                cuenta_new.id_persona = persona.id
                cuenta_new.guardar
                return cuenta_new.id
        else:
            return -1

    def modificar(self, data):
        personaS = Persona.query.filter_by(external_id =  data["external"]).first()
        if personaS:
            persona = Persona()
            persona.copy(personaS)
            persona.apellidos = data["apellidos"]
            persona.nombres = data["nombres"]
            
            persona.external_id = uuid.uuid4()
            #print(persona.serialize)
            persona.modificar
            return persona.id
        else:
            return -1
        
    def cambiar_estado(self, external):
        cuentaS = Cuenta.query.filter_by(external_id =  external).first()
        if cuentaS:
            cuenta = Cuenta()
            cuenta.copy(cuentaS)
            cuenta.estado = True if cuenta.estado == False else False            
            cuenta.external_id = uuid.uuid4()
            #print(persona.serialize)
            cuenta.modificar
            return cuenta.id
        else:
            return -1
        
    def inicio_sesion(self, data):
        cuentaA = Cuenta.query.filter_by(correo = data["correo"]).first()
        if(cuentaA):
            #TODO encriptar
            #if cuentaA.clave == data["password"]:
            if self.verificar_clave(cuentaA.clave, data["clave"]):
                token = jwt.encode(
                    {
                        "external": cuentaA.external_id,
                        "exp": datetime.utcnow() + timedelta(minutes=120)
                    },
                    key=current_app.config["SECRET_KEY"],
                    algorithm="HS512"
                )                
                cuenta = Cuenta()
                cuenta.copy(cuentaA)                
                
                persona = cuenta.getPersona(cuenta.id_persona)
                p1 = Persona()
                
                rol1 = p1.getRol(persona.id_rol)
                ex = cuentaA.external_id.encode()
                exBytes = base64.b64encode(ex)
                info = {
                    "token": token,
                    "external": exBytes.decode(),
                    "user": persona.apellidos+" "+persona.nombres,
                    "permiso": rol1.nombre
                }
                return  info
            else:
                return -4
        else:
            return -4

    def crear_roles(self):
        roles = Rol.query.all()
        if(len(roles)==0):
            rol = Rol()
            rol.descripcion="Es el administrador"
            rol.nombre = "ADMIN"
            rol.estado = True
            rol.external_id = uuid.uuid4()
            rol.guardar
            rol1 = Rol()
            rol1.descripcion="Es el usuario"
            rol1.nombre = "USER"
            rol1.estado = True
            rol1.external_id = uuid.uuid4()
            rol1.guardar
            p = {"apellidos":"Solano", "nombres":"Juan", "correo":"juan.solano@unl.edu.ec", "clave":"jc2024", "dni":"9999999999"}
            i = self.guardar(p)
            #print("GUARDO PEROSNA "+str(i))

    def verificar_clave(self, clave_hash, clave):
        return checkph(clave_hash, clave)
    
    def getPerfil(self, external):
        ext = base64.b64decode(external)
        #print(ext)
        cuentaA = Cuenta.query.filter_by(external_id = ext).first()
        if cuentaA:
            pers = Persona.query.filter_by(id = cuentaA.id_persona).first()
            return pers
        else:
            return None

    def modificar_perfil(self, data):
        ext = base64.b64decode(data["external"])
        cuentaA = Cuenta.query.filter_by(external_id = ext).first()
        if cuentaA:
            personaS = Persona.query.filter_by(id =  cuentaA.id_persona).first()
            if personaS:
                persona = Persona()
                persona.copy(personaS)
                persona.apellidos = data["apellidos"]
                persona.nombres = data["nombres"]            
                persona.external_id = uuid.uuid4()
                #print(persona.serialize)
                persona.modificar
                cuen = Cuenta()
                cuen.copy(cuentaA)
                cuen.clave = genph(data["clave"])
                cuen.external_id = uuid.uuid4()
                cuen.modificar
                return persona.id
            else:
                return -1
        else:
            return -2