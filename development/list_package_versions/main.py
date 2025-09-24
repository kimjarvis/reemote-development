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

class List_package_versions:
    def execute(self):
        r = yield Shell("apk info -v")
        print(r.cp.stdout.splitlines())
        result = [split_package_name_version(pkg) for pkg in r.cp.stdout.splitlines()]
        rows=[]
        for name, version in result:
            print(f"Name: {name}, Version: {version}")
            rows.append({"name": name, "version": version})
        out={"columnDefs": [{"headerName": "Name", "field": "name"},{"headerName": "Version", "field": "version"}],
             "rowData": rows}
        print(out)


async def main():
    responses = await execute(inventory(), List_package_versions())
    print(produce_table(produce_json(responses)))

if __name__ == "__main__":
    asyncio.run(main())