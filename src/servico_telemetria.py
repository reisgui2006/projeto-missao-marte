import json
import urllib.request

URL_ESTACAO = "https://estacao-terra.exemplo/api"


class ServicoTelemetriaEspacial:
    def _post(self, caminho, dados):
        req = urllib.request.Request(
            f"{URL_ESTACAO}/{caminho}",
            data=json.dumps(dados).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status

    def enviar_relatorio(self, status):
        return self._post("relatorio", status)

    def disparar_alerta(self, mensagem):
        return self._post("alerta", {"mensagem": mensagem})
