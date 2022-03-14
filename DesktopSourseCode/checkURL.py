def check_url(urlText):
    import requests
    try:
        a = requests.get(urlText)
        return True
    except InvalidURL as err:
        return False