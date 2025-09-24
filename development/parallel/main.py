import asyncio
from reemote.execute import execute
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
                'password': 'user'  # Password
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

class Get_versions:
    def execute(self):
        yield Shell("pip list --format=json")

async def main():
    import json
    responses = await execute(inventory(), Get_versions())

    host_packages = []
    host_names = []

    for i, r in enumerate(responses):
        host_name = r.host
        host_names.append(host_name)
        data = json.loads(r.cp.stdout)
        row = [{"name": pkg["name"], "version": pkg["version"]} for pkg in data]
        pkg_dict = {}
        for item in row:
            name, version = item["name"], item["version"]
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
    print(columnDefs,rowData)

if __name__ == "__main__":
    asyncio.run(main())