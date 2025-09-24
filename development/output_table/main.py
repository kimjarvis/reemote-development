import asyncio
from reemote.execute import execute
from reemote.produce_json import produce_json
from reemote.produce_output_table import produce_output_table
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

class Info_example:
    def execute(self):
        from reemote.operations.apk.info import Info
        # Get the package information on all hosts
        r = yield Info(package='vim')
        # View the package information
        print(r.cp.stdout)

class Hello_world:
    def execute(self):
        r = yield Shell("echo Hello World!")
        print(r.cp.stdout)

async def main():
    responses = await execute(inventory(), Info_example())
    print(produce_output_table(produce_json(responses)))


if __name__ == "__main__":
    asyncio.run(main())