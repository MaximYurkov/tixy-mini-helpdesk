from celery import shared_task
import requests
from rmq.cache import CacheManager

cache = CacheManager()


@shared_task
def fetch_cat_fact_task():
    cache_key = "api:cat_fact"

    if cache.exists(cache_key):
        return cache.get(cache_key)

    resp = requests.get("https://catfact.ninja/fact", timeout=5)
    resp.raise_for_status()

    data = resp.json()
    cache.set(cache_key, data, ttl=300)

    return data


@shared_task
def fetch_chuck_norris_task():
    cache_key = "api:chuck_norris"

    if cache.exists(cache_key):
        return cache.get(cache_key)

    resp = requests.get("https://api.chucknorris.io/jokes/random", timeout=5)
    resp.raise_for_status()

    data = resp.json()
    cache.set(cache_key, data, ttl=300)

    return data
