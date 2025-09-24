import asyncio
from reemote.execute import execute
from reemote.produce_json import produce_json
from reemote.produce_table import produce_table
from reemote.operations.server.shell import Shell

from typing import List, Tuple, Dict, Any

from typing import List, Tuple, Dict, Any

from typing import List, Tuple, Dict, Any

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


class Get_versions:
    def execute(self):
        yield Shell("""dpkg-query --showformat='{"name": "${Package}", "version": "${Version}"},' --show""")

async def main():
    import json
    responses = await execute(inventory(), Get_versions())

    host_packages = []
    host_names = []

    print(responses)

    for i, r in enumerate(responses):
        host_name = r.host
        host_names.append(host_name)
        data = json.loads("["+r.cp.stdout[:-1]+"]")
        row = [{"name": pkg["name"], "version": pkg["version"]} for pkg in data]
        pkg_dict = {}
        for item in row:
            name, version = item["name"], item["version"]
            pkg_dict[name] = version
        host_packages.append(pkg_dict)

if __name__ == "__main__":
    asyncio.run(main())