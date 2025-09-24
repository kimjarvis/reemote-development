import asyncio
from reemote.execute import execute
from reemote.produce_json import produce_json
from reemote.produce_table import produce_table
from reemote.operations.server.shell import Shell
from reemote.operation import Operation
from reemote.operations.apt.packages import Packages as apt_Packages
from reemote.operations.dpkg.packages import Packages as dpkg_Packages

from typing import List, Tuple, Dict, Any

def inventory() -> List[Tuple[Dict[str, Any], Dict[str, str]]]:
    return [
        (
            {
                'host': '192.168.122.143',  # debian
                'username': 'kim',  # User name
                'password': 'userpassword'  # Password
            },
            {
                'sudo_user': 'kim',
                'sudo_password': 'userpassword',
            }
        )
    ]


class Hello_world:
    def execute(self):
        r0 = yield apt_Packages(packages=["wget"], present=True, sudo=True)
        # print(r0)
        r1 = yield Shell("wget http://http.us.debian.org/debian/pool/main/r/rustc/cargo_1.85.0+dfsg3-1_amd64.deb")
        # print(r1)
        r2= yield dpkg_Packages(packages=["cargo_1.85.0+dfsg3-1_amd64.deb"], present=True, sudo=True)
        # print(r2)

async def main():
    responses = await execute(inventory(), Hello_world())
    print(produce_table(produce_json(responses)))

if __name__ == "__main__":
    asyncio.run(main())