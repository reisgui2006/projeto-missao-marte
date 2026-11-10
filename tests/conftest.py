import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.gerenciador_recursos import GerenciadorRecursosMarte


@pytest.fixture(scope="session")
def parametros_habitat():
    """Parâmetros iniciais do habitat (carregados uma vez)."""
    return {"oxigenio": 100, "agua": 200, "astronautas": 4}


@pytest.fixture
def telemetria_mock(mocker):
    """Dublê do ServicoTelemetriaEspacial: nenhuma chamada de rede real."""
    return mocker.MagicMock()


@pytest.fixture
def gerenciador(parametros_habitat, telemetria_mock):
    g = GerenciadorRecursosMarte(
        telemetria_mock, parametros_habitat["oxigenio"], parametros_habitat["agua"]
    )
    yield g  # preparação acima, limpeza abaixo
    g.oxigenio = 0
    g.agua = 0


@pytest.fixture
def driver():
    opcoes = Options()
    opcoes.add_argument("--headless=new")
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument("--window-size=1280,800")
    drv = webdriver.Chrome(options=opcoes)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Salva screenshot automaticamente quando um teste Selenium falha."""
    resultado = yield
    rep = resultado.get_result()
    if rep.when == "call" and rep.failed and "driver" in item.funcargs:
        os.makedirs("screenshots", exist_ok=True)
        item.funcargs["driver"].save_screenshot(f"screenshots/{item.name}.png")
