import pytest

from src.gerenciador_recursos import (
    NivelEmergenciaInvalidoError,
    OxigenioInsuficienteError,
)


@pytest.mark.parametrize(
    "astronautas, consumo, esperado",
    [(1, 0.84, 0.84), (4, 0.84, 3.36), (6, 1.0, 6.0), (0, 0.84, 0)],
)
def test_consumo_diario(gerenciador, astronautas, consumo, esperado):
    assert gerenciador.calcular_consumo_diario(astronautas, consumo) == pytest.approx(esperado)


@pytest.mark.parametrize("nivel, esperado", [(1, 10), (2, 15), (3, 20)])
def test_taxa_emergencia(gerenciador, nivel, esperado):
    assert gerenciador.calcular_taxa_emergencia(10, nivel) == esperado


@pytest.mark.parametrize("cota, esperado", [(1.0, 10), (0.5, 5), (0.25, 2.5)])
def test_racionamento(gerenciador, cota, esperado):
    assert gerenciador.aplicar_racionamento(10, cota) == esperado


@pytest.mark.parametrize("nivel", [0, 4, -1])
def test_nivel_emergencia_invalido(gerenciador, nivel):
    with pytest.raises(NivelEmergenciaInvalidoError):
        gerenciador.calcular_taxa_emergencia(10, nivel)


def test_oxigenio_insuficiente(gerenciador):
    with pytest.raises(OxigenioInsuficienteError):
        gerenciador.solicitar_oxigenio(500)


# ---- Mocks ----
def test_solicitacao_valida_envia_relatorio(gerenciador, telemetria_mock):
    gerenciador.solicitar_oxigenio(30)
    telemetria_mock.enviar_relatorio.assert_called_once_with({"oxigenio": 70, "agua": 200})
    telemetria_mock.disparar_alerta.assert_not_called()


def test_solicitacao_excessiva_dispara_alerta(gerenciador, telemetria_mock):
    with pytest.raises(OxigenioInsuficienteError):
        gerenciador.solicitar_oxigenio(500)
    telemetria_mock.disparar_alerta.assert_called_once_with(
        "Oxigênio insuficiente: solicitado 500, disponível 100"
    )


def test_resposta_simulada_da_estacao(mocker, gerenciador):
    gerenciador.telemetria = mocker.MagicMock()
    gerenciador.telemetria.enviar_relatorio.return_value = 200
    gerenciador.solicitar_oxigenio(10)
    gerenciador.telemetria.enviar_relatorio.assert_called_once_with({"oxigenio": 90, "agua": 200})
