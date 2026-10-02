# Shopify to Odoo/Logistics Integration Middleware (PoC)

Este repositorio contiene una **Prueba de Concepto (PoC)** modular desarrollada en **Python (Flask)** para la recepción, validación de seguridad y sanitización de datos de **Webhooks de Shopify Admin API** en arquitecturas de e-commerce e integración con ERPs (**Odoo**) o plataformas logísticas (MaaS).

## 🚀 Características Clave

* **Validación de Seguridad HMAC SHA256:** Verificación nativa del encabezado `X-Shopify-Hmac-Sha256` para garantizar que los datos provengan de Shopify.
* **Sanitización y Estandarización de Payloads:** Extracción y limpieza de estructuras JSON de órdenes de compra (Aduana de Datos).
* **Idempotencia y Manejo de Errores:** Control de duplicados e integración limpia mediante respuestas HTTP estándar.
* **Preparado para Serverless:** Arquitectura decoupled fácilmente adaptable a **AWS Lambda + API Gateway + Amazon SQS**.

## 🛠️ Requisitos e Instalación

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/edaroropeza/shopify-odoo-integration-poc.git](https://github.com/edaroropeza/shopify-odoo-integration-poc.git)
   cd shopify-odoo-integration-poc
