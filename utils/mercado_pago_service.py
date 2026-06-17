import os
import streamlit as st
import mercadopago


def _get_secret(nome: str):
    return os.getenv(nome) or st.secrets.get(nome)


class MercadoPagoService:
    def __init__(self):
        self.access_token = _get_secret("MERCADO_PAGO_ACCESS_TOKEN")
        self.app_url = _get_secret("APP_URL") or "https://aeterna.streamlit.app"
        self.sdk = mercadopago.SDK(self.access_token)

    def criar_checkout_plano(self, usuario_id: int, plano_nome: str, valor: float):
        preference_data = {
            "items": [{
                "title": f"aEterna - {plano_nome}",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(valor),
            }],
            "external_reference": f"usuario:{usuario_id}|plano:{plano_nome}",
            "back_urls": {
                "success": self.app_url,
                "failure": self.app_url,
                "pending": self.app_url,
            },
            "auto_return": "approved",
        }

        result = self.sdk.preference().create(preference_data)
        response = result.get("response", {})

        return response.get("init_point") or response.get("sandbox_init_point")