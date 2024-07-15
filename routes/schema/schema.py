from marshmallow import Schema, fields, ValidationError, validate
from util.validate import Trim, not_blank
class InicioSchema(Schema):
    correo = Trim(
        fields.Email(transform="upper"),
        validate=not_blank,
        required=True,
        error_messages={"required": "Se requiere el correo"},
    )
    clave = Trim(
        fields.String(transform="upper"),
        validate=not_blank,
        required=True,
        error_messages={"required": "Se requiere la clave"},
    )
class SitioSchema(Schema):
    nombre = Trim(
        fields.String(transform="upper"),
        validate=not_blank,
        required=True,
        error_messages={"required": "Se requiere el nombre"},
    )
    ubicacion = (
        Trim(
            fields.String(transform="upper"),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere la ubicacion"},
        )
    )
    fuente = Trim(
        fields.String(transform="upper"),
        validate=not_blank,
        required=True,
        error_messages={"required": "Se requiere la fuente"},
    )
    external_canton = (
        Trim(
            fields.String(),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere el external del canton"},
        )
    )
    longitud = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere la ubicacion"}
        )
    )
    latitud = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere la laltitud"}
        )
    )
    promedio = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere la ubicacion"}
        )
    )
    irradiacion = fields.Number(
        required=True, error_messages={"required": "Se requiere la laltitud"}
    )
#SHEMA EDIT
class SitioEditSchema(SitioSchema):
    
    external = (
        Trim(
            fields.String(),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere el external del sitio"},
        )
    )

class CensoSchema(Schema):
    enero = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor de enero"}
        )
    )
    febrero = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor de febrero"}
        )
    )
    marzo = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor de marzo"}
        )
    )
    abril = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor de abril"}
        )
    )
    mayo = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor de mayo"}
        )
    )
    junio = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor de junio"}
        )
    )
    julio = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor de julio"}
        )
    )
    agosto = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor de agosto"}
        )
    )
    septiembre = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor de septiembre"}
        )
    )
    octubre = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor de octubre"}
        )
    )
    noviembre = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor de noviembre"}
        )
    )
    diciembre = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor de diciembre"}
        )
    )
    promedio = (
        fields.Number(
            required=True, error_messages={"required": "Se requiere el valor del promedio"}
        )
    )
    external = (
        Trim(
            fields.String(),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere el external del sitio"},
        )
    )

#SHEMA PERSONA
#PERFIL
class PersonaPerfilSchema(Schema):
    
    external = (
        Trim(
            fields.String(),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere el external de la persona"},
        )
    )
    apellidos = (
        Trim(
            fields.String(),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere los apellidos de la persona"},
        )
    )
    nombres = (
        Trim(
            fields.String(),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere los nombres de la persona"},
        )
    )
    clave = (
        Trim(
            fields.String(),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere la clave de la cuenta"},
        )
    )

class PersonaGuardarSchema(Schema):
    
    correo = (
        Trim(
            fields.String(),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere el correo de la persona"},
        )
    )
    apellidos = (
        Trim(
            fields.String(),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere los apellidos de la persona"},
        )
    )
    nombres = (
        Trim(
            fields.String(),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere los nombres de la persona"},
        )
    )
    dni = (
        Trim(
            fields.String(),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere el dni"},
        )
    )
    clave = (
        Trim(
            fields.String(),
            validate=not_blank,
            required=True,
            error_messages={"required": "Se requiere su clave"},
        )
    )