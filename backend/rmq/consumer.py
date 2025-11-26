import pika
import os
import requests
import json
import sys

def get_vault_secret(path: str, key: str):
    url = f"{os.environ['VAULT_ADDR']}/v1/{path}"
    token = os.environ['VAULT_TOKEN']

    resp = requests.get(
        url,
        headers={"X-Vault-Token": token},
        timeout=5
    )
    return resp.json()["data"]["data"][key]

def handle_cat_fact():
    resp = requests.get("https://catfact.ninja/fact", timeout=5)
    data = resp.json()
    with open("cat_fact.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("[✔] Cat fact saved")

def callback(ch, method, properties, body):
    print("[x] Received:", body.decode())

    msg = json.loads(body)

    if msg["task"] == "cat_fact":
        handle_cat_fact()

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    queue_name = sys.argv[1] if len(sys.argv) > 1 else "cat_queue"

    rabbit_user = "tixy_rabbit"
    rabbit_pass = get_vault_secret("minihelpdesk/rabbitmq", "password")

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

    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(
        exchange="tixy_exchange",
        queue=queue_name,
        routing_key=queue_name
    )

    print(f"[*] Listening queue {queue_name}...")
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


if __name__ == "__main__":
    main()
