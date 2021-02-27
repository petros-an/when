from app.models import *
import requests
import shutil

dir = "images"


def download_image(url, id):
    suffix = url.split(".")[-1]
    response = requests.get("https://" + url)
    with open(f"{dir}/{id}.{suffix}", "wb") as out_file:
        out_file.write(response.content)

def run():
    for e in Event.objects.all():
        img_url = e.info['url']
        download_image(img_url, e.id)