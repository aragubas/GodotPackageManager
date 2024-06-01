import json
from io import StringIO

from GodotAPI import getPackage
from Package import Package, PackageEncoder


def get_packages(path: str) -> list[Package]:
    with open(path) as file:
        packageFile = file.read()

    packagesJson = json.load(StringIO(packageFile))
    packages = list()

    for key, value in packagesJson.items():
        package = Package(key, value["name"], value["version"])
        packages.append(package)

    return packages


def write_packages(path: str, packages: list[Package]):
    # Re-serialize list to correct format
    dataToSerialize = {}

    for package in packages:
        dataToSerialize[package.id] = {"name": package.name, "version": package.version}

    fileData = json.dumps(dataToSerialize, sort_keys=True, cls=PackageEncoder, indent=2)

    with open(path, "w") as file:
        file.write(fileData)


def add_package(path: str, package: Package):
    packed_packages = get_packages(path)

    # Check if package with same name or url exists
    for packed in packed_packages:
        # Found similar package, stop
        if packed.id == package.id:
            raise FileExistsError('Package "%s" already exists' % packed.name)

    # No similar package found
    packed_packages.append(package)

    write_packages(path, packed_packages)


def remove_package(path: str, package_id: str):
    packed_packages = get_packages(path)

    i = 0
    package_found = False
    for package in packed_packages:
        if package.id == package_id:
            package_found = True
            break
        i += 1

    if not package_found:
        raise FileNotFoundError("Could not find package with ID '%s'." % package_id)

    packed_packages.pop(i)

    write_packages(path, packed_packages)


if __name__ == "__main__":
    path = "./packages.json"

    # TEST: Get package from the Asset Library API
    # pkg = getPackage(2652)
    # print(pkg)

    # TEST: Add test package
    # newPackage = Package("2604", "Post Process", "0.1.0")
    # add_package(path, newPackage)

    # TEST: Remove test package
    # remove_package(path, "2604")

    print("Packages in packages.json:")
    for package in get_packages(path):
        print("'%s'" % package.name)
        print("  ID: '%s'" % package.id)
        print("  Version: '%s'" % package.version)
