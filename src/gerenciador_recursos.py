class OxigenioInsuficienteError(Exception):
    """Estoque de oxigênio menor que o solicitado."""


class NivelEmergenciaInvalidoError(Exception):
    """Nível de emergência fora do intervalo 1-3."""


MULTIPLICADOR_EMERGENCIA = {1: 1.0, 2: 1.5, 3: 2.0}


class GerenciadorRecursosMarte:
    def __init__(self, telemetria, oxigenio, agua):
        self.telemetria = telemetria
        self.oxigenio = oxigenio
        self.agua = agua

    def calcular_consumo_diario(self, astronautas, consumo_por_astronauta):
        return astronautas * consumo_por_astronauta

    def calcular_taxa_emergencia(self, consumo, nivel):
        if nivel not in MULTIPLICADOR_EMERGENCIA:
            raise NivelEmergenciaInvalidoError(f"Nível inválido: {nivel}")
        return consumo * MULTIPLICADOR_EMERGENCIA[nivel]

    def aplicar_racionamento(self, consumo, cota):
        """Limita o consumo à cota (0 < cota <= 1) do valor original."""
        return consumo * cota

    def solicitar_oxigenio(self, quantidade):
        if quantidade > self.oxigenio:
            self.telemetria.disparar_alerta(
                f"Oxigênio insuficiente: solicitado {quantidade}, disponível {self.oxigenio}"
            )
            raise OxigenioInsuficienteError("Oxigênio insuficiente")
        self.oxigenio -= quantidade
        self.telemetria.enviar_relatorio({"oxigenio": self.oxigenio, "agua": self.agua})
        return self.oxigenio
