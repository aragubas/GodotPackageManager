import json
from io import StringIO
from json import JSONEncoder

class Package:
    url = ""
    name = ""

    def __init__(self, url, name):
        self.url = url
        self.name = name


class PackageEncoder(JSONEncoder):
    def default(self, object):
        return { object.name: { "url": object.url } }


def get_packages(path: str) -> list[Package]:
    with open(path) as file:
        packageFile = file.read()
    
    packagesJson = json.load(StringIO(packageFile))
    packages = list()
    
    print("packages type")
    print(type(packagesJson))

    for key, value in packagesJson.items():
        package = Package(value["url"], key)
        packages.append(package)

    return packages


def write_packages(path: str, packages: list[Package]):
    # Re-serialize list to correct format
    dataToSerialize = { }

    for package in packages:
        dataToSerialize[package.name] = { "url": package.url }

    fileData = json.dumps(dataToSerialize, sort_keys=True, cls=PackageEncoder, indent=2)

    with open(path, 'w') as file:
        file.write(fileData)


def add_package(path: str, package: Package):
    packed_packages = get_packages(path)

    # Check if package with same name or url exists
    for packed in packed_packages:
        # Found similar package, stop
        if packed.name == package.name or packed.url == package.url:
            raise FileExistsError("Package \"%s\" already exists" % packed.name)
    
    # No similar package found
    packed_packages.append(package)

    write_packages(path, packed_packages)


def remove_package(path: str, package: Package):
    pass


if __name__ == "__main__":
    path = "./packages.json"

    print("Packages in packages.json:")    
    for package in get_packages(path):
        print(package.name)

    # TEST: Add test package
    #newPackage = Package("https://github.com/caldo enceirasticos", "third package")
    #add_package(path, newPackage)

    