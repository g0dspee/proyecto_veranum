from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.webpay.webpay_plus.transaction import WebpayOptions
from transbank.common.integration_type import IntegrationType

# Configuración para modo integración
def get_transaction():
    return Transaction(WebpayOptions(
        commerce_code='597055555532',
        api_key='test',  # Puedes usar 'test' como api_key en el entorno de integración
        integration_type=IntegrationType.TEST
    ))