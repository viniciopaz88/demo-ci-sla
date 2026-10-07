import pytest

from sla import prioridad, cumple_sla, tiempo_restante_sla


# ---------- prioridad ----------

def test_impacto_alto_urgencia_alta_es_P1():
    assert prioridad(1, 1) == "P1"


def test_impacto_medio_urgencia_baja_es_P4():
    assert prioridad(2, 3) == "P4"


def test_impacto_fuera_de_rango_lanza_error():
    with pytest.raises(ValueError):
        prioridad(5, 1)


# ---------- cumple_sla ----------

def test_P1_resuelto_en_3_horas_cumple():
    assert cumple_sla("P1", 180) is True


def test_P2_resuelto_en_10_horas_no_cumple():
    assert cumple_sla("P2", 600) is False


def test_prioridad_inexistente_lanza_error():
    with pytest.raises(ValueError):
        cumple_sla("P9", 30)


def test_tiempo_negativo_lanza_error():
    with pytest.raises(ValueError):
        cumple_sla("P1", -10)


# ---------- tiempo_restante_sla ----------

def test_P2_con_5_horas_transcurridas_quedan_180_minutos():
    assert tiempo_restante_sla("P2", 300) == 180


def test_P3_recien_abierto_tiene_24_horas():
    assert tiempo_restante_sla("P3", 0) == 1440


def test_sla_vencido_retorna_cero_y_no_negativo():
    assert tiempo_restante_sla("P1", 500) == 0
