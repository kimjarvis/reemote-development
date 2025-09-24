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
        )
    ]


class Get_versions:
    def execute(self):
        yield Shell("dnf list installed")

async def main():
    import re
    responses = await execute(inventory(), Get_versions())
    print(responses)

    import re

    host_packages = []
    host_names = []

    # Fixed regex: capture package name (non-whitespace), then skip whitespace, then capture version (non-whitespace)
    pattern = r'^(\S+)\s+(\S+)'

    for i, r in enumerate(responses):
        host_name = r.host
        host_names.append(host_name)
        pkg_dict = {}

        lines = r.cp.stdout.strip().split('\n')[1:]  # ← ADJUST THIS IF NEEDED

        for line in lines:
            match = re.match(pattern, line)
            if match:
                package_name = match.group(1)
                version = match.group(2)
                pkg_dict[package_name] = version

        host_packages.append(pkg_dict)
        print(host_packages)  # You may want to print per host or move outside loop


if __name__ == "__main__":
    asyncio.run(main())