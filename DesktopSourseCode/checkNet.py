import requests


def connected_to_internet(url='http://www.google.com/', timeout=5):
    try:
        a = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
