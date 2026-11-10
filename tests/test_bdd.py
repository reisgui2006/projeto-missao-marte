import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.gerenciador_recursos import GerenciadorRecursosMarte, OxigenioInsuficienteError

scenarios("features/solicitacao_oxigenio.feature")


@pytest.fixture
def contexto():
    return {}


@given(parsers.parse("o habitat possui {qtd:d} unidades de oxigênio"), target_fixture="habitat")
def habitat(qtd, telemetria_mock):
    return GerenciadorRecursosMarte(telemetria_mock, qtd, 200)


@when(parsers.parse("o astronauta solicita {qtd:d} unidades"))
def solicitar(habitat, contexto, qtd):
    try:
        habitat.solicitar_oxigenio(qtd)
    except OxigenioInsuficienteError as erro:
        contexto["erro"] = erro


@then(parsers.parse("o estoque restante é de {qtd:d} unidades"))
def verifica_estoque(habitat, qtd):
    assert habitat.oxigenio == qtd


@then("nenhum alerta é enviado à Terra")
def sem_alerta(telemetria_mock):
    telemetria_mock.disparar_alerta.assert_not_called()


@then("ocorre um erro de oxigênio insuficiente")
def verifica_erro(contexto):
    assert isinstance(contexto.get("erro"), OxigenioInsuficienteError)


@then("um alerta de emergência é enviado à Terra")
def alerta_enviado(telemetria_mock):
    telemetria_mock.disparar_alerta.assert_called_once_with(
        "Oxigênio insuficiente: solicitado 500, disponível 100"
    )
