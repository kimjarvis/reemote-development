import asyncio
from reemote.execute import execute
from reemote.operations.filesystem.get_file import Get_file
from reemote.produce_json import produce_json
from reemote.produce_table import produce_table
from reemote.operations.server.shell import Shell

from typing import List, Tuple, Dict, Any

def inventory() -> List[Tuple[Dict[str, Any], Dict[str, str]]]:
     return [
        (
            {
                'host': '10.156.135.16',  # alpine
                'username': 'user',  # User name
                'password': 'user',  # Password
                'env': {'LANG': 'en_GB','LC_COLLATE': 'C'}
            },
            {
                'su_user': 'root',
                'su_password': 'root'  # Password
            }
        ),
        (
            {
                'host': '10.156.135.19',  # alpine
                'username': 'user',  # User name
                'password': 'user'  # Password
            },
            {
                'su_user': 'root',
                'su_password': 'root'  # Password
            }
        )
    ]

def split_package_name_version(self,pkg_str):
    import re
    # Match from end: <version>-r<number>
    # We want to split at the LAST hyphen before "-r<number>"
    parts = pkg_str.rsplit('-', 2)  # Split into at most 3 parts, from the right
    if len(parts) == 3 and re.match(r'^r\d+$', parts[2]):
        name = parts[0]
        version = parts[1] + '-' + parts[2]
        return name, version
    else:
        # Fallback: if format doesn't match, return whole string as name, empty version
        return pkg_str, ""

def list_package_versions(responses):
    # Parse packages for each host
    host_packages = []
    host_names = []

    for i, r in enumerate(responses):
        host_name = r.host
        host_names.append(host_name)
        pkgs = r.cp.stdout.splitlines()
        pkg_dict = {}
        for pkg in pkgs:
            name, version = split_package_name_version(pkg)
            pkg_dict[name] = version
        host_packages.append(pkg_dict)

    # Get all unique package names across all hosts
    all_package_names = set()
    for pkg_dict in host_packages:
        all_package_names.update(pkg_dict.keys())
    all_package_names = sorted(all_package_names)

    # Build column definitions: Name + one per host
    columnDefs = [{"headerName": "Package Name", "field": "name"}]
    for host_name in host_names:
        columnDefs.append({"headerName": host_name, "field": host_name.replace(".","_")})

    # Build row data
    rowData = []
    for pkg_name in all_package_names:
        row = {"name": pkg_name}
        for i, host_name in enumerate(host_names):
            row[host_name.replace(".","_")] = host_packages[i].get(pkg_name, "")  # empty if not installed
        rowData.append(row)

    # Store in app.storage
    return columnDefs,rowData


def split_package_name_version(pkg_str):
    import re
    # Match from end: <version>-r<number>
    # We want to split at the LAST hyphen before "-r<number>"
    parts = pkg_str.rsplit('-', 2)  # Split into at most 3 parts, from the right
    if len(parts) == 3 and re.match(r'^r\d+$', parts[2]):
        name = parts[0]
        version = parts[1] + '-' + parts[2]
        return name, version
    else:
        # Fallback: if format doesn't match, return whole string as name, empty version
        return pkg_str, ""


class Hello_world:
    def execute(self):
        import json
        from reemote.operations.filesystem.get_file import Get_file
        from reemote.operations.filesystem.put_file import Put_file
        # from reemote.operations.apk.packages import Packages
        # r = yield Shell(f"echo Hello World!")
        # print(r)
        # print(r.host)
        # print(r.op.global_info)
        # r = yield Put_file(path="example.txt", text="Hello World!")
        # r = yield Packages(packages=["sudo"],present=True, su=True)
        # r = yield Get_file(path="/etc/sudoers",host="10.156.135.16")
        # r = yield Packages(packages=["python3","py3-pip"], present=True, su=True)
        # print(r)
        # r = yield Shell("pip list --format=json")
        #
        # import json
        # data = json.loads(r.cp.stdout)
        # rows = [{"name": pkg["name"], "version": pkg["version"]} for pkg in data]

        # for name, version in result:
        #     print(f"Name: {name}, Version: {version}")
        #     rows.append({"name": name, "version": version})
        # out={"columnDefs": [{"headerName": "Name", "field": "name"},{"headerName": "Version", "field": "version"}],
        #      "rowData": rows}
        # print(out)
        # r = yield Shell("apk info -v")
        r = yield Shell("pip list --format=json")
        data = json.loads(r.cp.stdout)
        rows = [{"name": pkg["name"], "version": pkg["version"]} for pkg in data]
        print(rows)
        # print(r)
        # columnDefs,rowData=list_package_versions([r])
        # print(columnDefs,rowData)

async def main():
    responses = await execute(inventory(), Hello_world())
    list_package_versions(responses)
    print(produce_table(produce_json(responses)))


if __name__ == "__main__":
    asyncio.run(main())