"""Funciones de una mesa de servicio: prioridad y acuerdos de nivel de servicio (SLA).

Impacto y urgencia se expresan de 1 a 3:
    1 = alto, 2 = medio, 3 = bajo
"""

# Matriz de prioridad: MATRIZ[impacto][urgencia]
MATRIZ = {
    1: {1: "P0", 2: "P2", 3: "P3"},
    2: {1: "P2", 2: "P3", 3: "P4"},
    3: {1: "P3", 2: "P4", 3: "P4"},
}

# Tiempo máximo de resolución por prioridad, en minutos
SLA_MINUTOS = {
    "P1": 240,    # 4 horas
    "P2": 480,    # 8 horas
    "P3": 1440,   # 24 horas
    "P4": 4320,   # 72 horas
}


def prioridad(impacto, urgencia):
    """Retorna la prioridad (P1 a P4) según la matriz impacto x urgencia."""
    if impacto not in MATRIZ or urgencia not in MATRIZ[1]:
        raise ValueError("Impacto y urgencia deben ser 1, 2 o 3")
    return MATRIZ[impacto][urgencia]


def cumple_sla(prioridad, minutos_resolucion):
    """Retorna True si el ticket se resolvió dentro del tiempo de su prioridad."""
    if prioridad not in SLA_MINUTOS:
        raise ValueError(f"Prioridad desconocida: {prioridad}")
    if minutos_resolucion < 0:
        raise ValueError("El tiempo de resolución no puede ser negativo")
    return minutos_resolucion <= SLA_MINUTOS[prioridad]


def tiempo_restante_sla(prioridad, minutos_transcurridos):
    """Retorna los minutos que quedan antes de incumplir el SLA (nunca negativo)."""
    if prioridad not in SLA_MINUTOS:
        raise ValueError(f"Prioridad desconocida: {prioridad}")
    if minutos_transcurridos < 0:
        raise ValueError("El tiempo transcurrido no puede ser negativo")
    return max(0, SLA_MINUTOS[prioridad] - minutos_transcurridos)
