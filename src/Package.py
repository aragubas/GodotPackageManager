from json import JSONEncoder

class Package:
    id = ""
    name = ""
    version = "0.0.0"

    def __init__(self, id, name, version):
        self.id = id
        self.name = name
        self.version = version

class PackageEncoder(JSONEncoder):
    def default(self, object):
        if object is Package:        
            return { object.id: { "name": object.name, "version": object.version } }
        
        return super().default(object)
