from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PAINEL = (Path(__file__).parent.parent / "web" / "painel.html").resolve().as_uri()


def solicitar(driver, quantidade):
    driver.get(PAINEL)
    driver.find_element(By.ID, "quantidade").send_keys(str(quantidade))
    driver.find_element(By.ID, "solicitar").click()


def test_solicitacao_oxigenio_atualiza_nivel(driver):
    solicitar(driver, 30)
    espera = WebDriverWait(driver, 5)
    espera.until(EC.text_to_be_present_in_element((By.ID, "nivel-oxigenio"), "70"))
    espera.until(EC.text_to_be_present_in_element((By.ID, "mensagem"), "aprovada"))
    assert driver.find_element(By.ID, "nivel-oxigenio").text == "70"


def test_solicitacao_acima_do_estoque_exibe_erro(driver):
    solicitar(driver, 500)
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "mensagem"), "insuficiente")
    )
    assert driver.find_element(By.ID, "nivel-oxigenio").text == "100"
