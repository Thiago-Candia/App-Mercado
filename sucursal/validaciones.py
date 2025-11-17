from rest_framework import serializers

def limpiar_texto(valor=None) -> str:
    return "" if valor is None else str(valor).strip()

def colapsar_espacios(valor: str) -> str:
    return " ".join(str(valor).split())

def solo_digitos(valor) -> str:
    return "".join(ch for ch in str(valor) if ch.isdigit())

def dni_valido(valor=None) -> bool:
    if valor is None:
        return False
    return len(valor) in (6, 7, 8) and valor.isdigit()

def telefono_valido(valor=None) -> bool:
    if valor is None:
        return False
    return 9 <= len(valor) <= 15 and str(valor).isdigit()

def es_mail_valido(valor=None) -> bool:
    if valor is None:
        return False
    return 5 <= len(valor) <= 120 and ("@" in valor and "." in valor)

def es_nombre_valido(valor=None) -> bool:
    permitidos = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "áéíóúüñÁÉÍÓÚÜÑ"
    "àèìòùÀÈÌÒÙ"
    "âêîôûÂÊÎÔÛ"
    "äëïöüÿÄËÏÖÜŸ"
    "ãõÃÕ"
    "çÇ"
    " -'."
    )
    if valor is None:
        return False
    if 2 <= len(valor) <= 50:
        return all(ch in permitidos for ch in valor)
    return False

def pedir_nombre_hasta_valido(valor=None) -> str:
    nombre = colapsar_espacios(limpiar_texto(valor))
    while not es_nombre_valido(nombre):
        raise serializers.ValidationError("nombre invalido")
    return nombre.upper()

def pedir_mail_hasta_valido(valor=None) -> str:
    mail = (limpiar_texto(valor))
    while not es_mail_valido(mail):
        raise serializers.ValidationError("email invalido")
    return mail.lower()


def pedir_telefono_hasta_valido(valor=None) -> str:
    telefono = solo_digitos(limpiar_texto(valor))
    while not telefono_valido(telefono):
        raise serializers.ValidationError("Teléfono inválido.")
    return telefono

def pedir_dni_hasta_valido(valor=None) -> str:
    dni = solo_digitos(limpiar_texto(valor))
    while not dni_valido(dni):
        raise serializers.ValidationError("DNI invalido (6 a 8 dígitos, sin puntos ni espacios): ")
    return dni