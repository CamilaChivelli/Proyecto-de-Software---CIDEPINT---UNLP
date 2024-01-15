"""
Enumerable para el tipo de servicio.
"""
import enum


class ServiceTypeEnum(enum.Enum):
    ANALISIS = "Análisis"
    CONSULTORIA = "Consultoría"
    DESARROLLO = "Desarrollo"
