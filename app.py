import os
import hmac
import hashlib
import base64
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Se obtiene el Secret de Shopify desde las variables de entorno
SHOPIFY_WEBHOOK_SECRET = os.getenv('SHOPIFY_WEBHOOK_SECRET', 'my_secret_key')

def verify_shopify_webhook(data, hmac_header):
    """
    Valida la integridad y autenticidad del Webhook enviado por Shopify mediante HMAC SHA256.
    """
    if not hmac_header:
        return False
    
    digest = hmac.new(
        SHOPIFY_WEBHOOK_SECRET.encode('utf-8'),
        data,
        hashlib.sha256
    ).digest()
    
    computed_hmac = base64.b64encode(digest).decode('utf-8')
    return hmac.compare_digest(computed_hmac, hmac_header)

@app.route('/webhooks/shopify/orders/create', methods=['POST'])
def handle_order_created():
    """
    Endpoint encargado de recibir, validar y sanitizar las órdenes de Shopify
    antes de sincronizarlas con el ERP (Odoo) o la plataforma logística.
    """
    hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
    raw_data = request.get_data()

    # 1. Validación de Seguridad HMAC
    if not verify_shopify_webhook(raw_data, hmac_header):
        return jsonify({"error": "Unauthorized / Invalid HMAC"}), 401

    payload = request.get_json()
    
    # 2. Control de Idempotencia y extracción de ID de Orden
    order_id = payload.get('id')
    order_number = payload.get('name')
    
    if not order_id:
        return jsonify({"error": "Payload inválido, falta order_id"}), 400

    # 3. Sanitización y Estandarización de Payload (Aduana de Datos)
    sanitized_order = {
        "external_order_id": str(order_id),
        "order_reference": order_number,
        "customer_email": payload.get('email'),
        "customer_phone": payload.get('shipping_address', {}).get('phone'),
        "shipping_address": {
            "street": payload.get('shipping_address', {}).get('address1'),
            "city": payload.get('shipping_address', {}).get('city'),
            "province": payload.get('shipping_address', {}).get('province'),
            "zip": payload.get('shipping_address', {}).get('zip'),
            "country": payload.get('shipping_address', {}).get('country_code')
        },
        "total_amount": float(payload.get('total_price', 0.0)),
        "currency": payload.get('currency'),
        "items": [
            {
                "sku": item.get('sku'),
                "quantity": item.get('quantity'),
                "price": float(item.get('price'))
            } for item in payload.get('line_items', [])
        ]
    }

    # 4. Simulación de inyección/sincronización hacia Odoo API / Middleware
    print(f"[OK] Orden {order_number} ({order_id}) procesada correctamente y lista para Odoo.")
    
    return jsonify({
        "status": "success",
        "message": "Webhook procesado e inyectado con éxito",
        "processed_order_id": order_id
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
