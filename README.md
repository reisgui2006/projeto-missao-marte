[![Pipeline](https://github.com/reisgui2006/projeto-missao-marte/actions/workflows/pipeline.yml/badge.svg)](https://github.com/reisgui2006/projeto-missao-marte/actions/workflows/pipeline.yml)

# Missão Marte: ECLSS – Automação de Testes

Suíte de testes do módulo de controle do habitat de Marte (pytest, pytest-mock, Selenium headless, pytest-bdd e GitHub Actions).

## Executando localmente

Requisito: Python 3.10+ e Google Chrome instalado.

```bash
git clone https://github.com/SEU_USUARIO/projeto-missao-marte.git
cd projeto-missao-marte
pip install -r requirements.txt
pytest
```

O relatório de cobertura é exibido no console. Screenshots de falhas do Selenium são salvos em `screenshots/`.
