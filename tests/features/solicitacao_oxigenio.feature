Feature: Solicitação de oxigênio
  Como astronauta do habitat
  Quero solicitar oxigênio extra
  Para manter o suporte de vida

  Scenario: Solicitação em condições normais
    Given o habitat possui 100 unidades de oxigênio
    When o astronauta solicita 30 unidades
    Then o estoque restante é de 70 unidades
    And nenhum alerta é enviado à Terra

  Scenario: Solicitação em situação de crise
    Given o habitat possui 100 unidades de oxigênio
    When o astronauta solicita 500 unidades
    Then ocorre um erro de oxigênio insuficiente
    And um alerta de emergência é enviado à Terra
