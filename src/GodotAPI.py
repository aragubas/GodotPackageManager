import http.client

req = http.client.HTTPSConnection("godotengine.org")


def request(method: str, endpoint: str, body=None, headers={}):
    try:
        req.request(method, f"/asset-library/api{endpoint}", body, headers)

        res = req.getresponse()
        data = res.read().decode("utf-8")

        return data
    except Exception as x:
        print(x)


def getPackage(id: int):
    package = request("GET", f"/asset/{id}")

    return package
