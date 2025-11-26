from celery import shared_task
import requests


@shared_task
def fetch_cat_fact_task():
    resp = requests.get("https://catfact.ninja/fact", timeout=5)
    resp.raise_for_status()
    return resp.json()


@shared_task
def fetch_chuck_norris_task():
    resp = requests.get("https://api.chucknorris.io/jokes/random", timeout=5)
    resp.raise_for_status()
    return resp.json()
