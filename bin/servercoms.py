import requests

class ServerComs:
    def __init__(self):
        pass

    def connect(self, url):
        try:
            self.x = requests.get(f"{url}/tryconnect")
            return True
        except Exception:
            return False

    def postcurrentsong(self, url, data):
        try:
            self.x = requests.post(f"{url}/postcurrentsong", {"songname":data})
            return True
        except Exception:
            return False

    def postupcomingsongs(self, url, data):
        try:
            self.x = requests.post(f"{url}/postupcomingsongs", {"songs":data})
            return True
        except Exception:
            return False

    def postplaybackpos(self, url, data):
        try:
            self.x = requests.post(f"{url}/postplayback", {"pos":data})
            return True
        except Exception:
            return False

    def postsonglength(self, url, data):
        try:
            self.x = requests.post(f"{url}/postsonglength", {"length":data})
            return True
        except Exception:
            return False

    def changefullscreen(self, url):
        try:
            self.x = requests.get(f"{url}/changefullscreen")
            return True
        except Exception:
            return False

    def getfullscreeninfo(self, url):
        try:
            self.x = requests.get(f"{url}/changefullscreen")
        except Exception:
            pass
        return self.x.text

    def poststatus(self, url, isalive):
        print("updating status")
        try:
            self.x = requests.post(f"{url}/poststatus", {"status":f"{isalive}"})
            return True
        except Exception:
            return False
