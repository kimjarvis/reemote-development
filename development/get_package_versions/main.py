import asyncio
from reemote.execute import execute
from reemote.produce_json import produce_json
from reemote.produce_table import produce_table

# from reemote.facts.apt.get_packages import Get_packages
# from reemote.facts.apk.get_packages import Get_packages
# from reemote.facts.dnf.get_packages import Get_packages
# from reemote.facts.dpkg.get_packages import Get_packages
# from reemote.facts.yum.get_packages import Get_packages
from reemote.facts.pip.get_packages import Get_packages
from tabulate import tabulate

from typing import List, Tuple, Dict, Any
# Alpine
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

# Centos
from typing import List, Tuple, Dict, Any

def inventory() -> List[Tuple[Dict[str, Any], Dict[str, str]]]:
     return [
        (
            {
                'host': '10.156.135.217',  # alpine
                'username': 'user',  # User name
                'password': 'user',  # Password
            },
            {
                'su_user': 'root',
                'su_password': 'root',  # Password
                'sudo_user': 'user',
                'sudo_password': 'user',  # Password
            }
        ),
        (
            {
                'host': '10.156.135.110',  # alpine
                'username': 'user',  # User name
                'password': 'user',  # Password
            },
            {
                'su_user': 'root',
                'su_password': 'root',  # Password
                'sudo_user': 'user',
                'sudo_password': 'user',  # Password
            }
        )
    ]

from typing import List, Tuple, Dict, Any


from typing import List, Tuple, Dict, Any
# Centos
from typing import List, Tuple, Dict, Any

def inventory() -> List[Tuple[Dict[str, Any], Dict[str, str]]]:
     return [
        (
            {
                'host': '10.156.135.217',  # alpine
                'username': 'user',  # User name
                'password': 'user',  # Password
            },
            {
                'su_user': 'root',
                'su_password': 'root',  # Password
                'sudo_user': 'user',
                'sudo_password': 'user',  # Password
            }
        ),
        (
            {
                'host': '10.156.135.110',  # alpine
                'username': 'user',  # User name
                'password': 'user',  # Password
            },
            {
                'su_user': 'root',
                'su_password': 'root',  # Password
                'sudo_user': 'user',
                'sudo_password': 'user',  # Password
            }
        )
    ]

# Ubuntu
def inventory() -> List[Tuple[Dict[str, Any], Dict[str, str]]]:
     return [
        (
            {
                'host': '10.156.135.164',  # alpine
                'username': 'user',  # User name
                'password': 'user',  # Password
            },
            {
                'su_user': 'root',
                'su_password': 'root',  # Password
                'sudo_user': 'user',
                'sudo_password': 'user',  # Password
            }
        ),
        (
            {
                'host': '10.156.135.148',  # alpine
                'username': 'user',  # User name
                'password': 'user',  # Password
            },
            {
                'su_user': 'root',
                'su_password': 'root',  # Password
                'sudo_user': 'user',
                'sudo_password': 'user',  # Password
            }
        )
    ]


async def main():
    responses = await execute(inventory(), Get_packages())
    print(produce_table(produce_json(responses)))
    print(responses)
    host_packages = []
    host_names = []

    for i, r in enumerate(responses):
        # print(r.cp.stdout)
        host_name = r.host
        host_names.append(host_name)
        pkg_dict = {}
        for v in r.cp.stdout:
            pkg_dict[v["name"]] = v["version"]
        host_packages.append(pkg_dict)

    # print(host_packages)
    # print(host_names)


    # Get all unique package names across all hosts
    all_package_names = set()
    for pkg_dict in host_packages:
        all_package_names.update(pkg_dict.keys())
    all_package_names = sorted(all_package_names)
    # print(all_package_names)


    # Build column definitions: Name + one per host
    columnDefs = [{"headerName": "Package Name", "field": "name", 'filter': 'agTextColumnFilter', 'floatingFilter': True}]
    for host_name in host_names:
        columnDefs.append({"headerName": host_name, "field": host_name.replace(".", "_")})

    # Build row data
    rowData = []
    for pkg_name in all_package_names:
        row = {"name": pkg_name}
        for i, host_name in enumerate(host_names):
            row[host_name.replace(".", "_")] = host_packages[i].get(pkg_name, "")  # empty if not installed
        rowData.append(row)

    # print(columnDefs)
    # print(rowData)

    # Step 1: Extract headers (use headerName if available, else field)
    headers = [col.get("headerName", col["field"]) for col in columnDefs]

    # Step 2: Extract rows — each row is a list of values in column order
    rows = []
    for row in rowData:
        row_data = [row.get(col["field"], "") for col in columnDefs]
        rows.append(row_data)

    # Step 3: Print table using tabulate
    print(tabulate(rows, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    asyncio.run(main())