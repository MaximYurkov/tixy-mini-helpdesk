import json
import pika
import requests
import os

def get_vault_secret(path: str, key: str):
    """Получение секрета из Vault через HTTP API."""
    url = f"{os.environ['VAULT_ADDR']}/v1/{path}"
    token = os.environ['VAULT_TOKEN']

    resp = requests.get(
        url,
        headers={"X-Vault-Token": token},
        timeout=5
    )
    data = resp.json()
    return data["data"]["data"][key]

def main():
    #пароль из Vault
    rabbit_user = "tixy_rabbit"
    rabbit_pass = get_vault_secret("minihelpdesk/rabbitmq", "password")

    #Соединение c RabbitMQ
    credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.environ["RABBIT_HOST"],
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange="tixy_exchange",
        exchange_type="direct",
        durable=True
    )

    #Пример сообщения
    message = {
        "task": "cat_fact",
        "params": {}
    }

    channel.basic_publish(
        exchange="tixy_exchange",
        routing_key="cat_queue",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2  
    )

    print(" [x] Sent:", message)
    connection.close()


if __name__ == "__main__":
    main()
