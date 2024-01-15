"""
Enumerable para el estado de la solicitud de servicio.
"""
import enum

class StatusEnum(enum.Enum):
    ACEPTADA = "Aceptada"
    CANCELADA = "Cancelada"
    EN_PROGRESO = "En progreso"
    FINALIZADA = "Finalizada"
    RECHAZADA = "Rechazada"



