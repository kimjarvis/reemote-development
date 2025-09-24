import asyncio

from reemote.operations.filesystem.mkdir1 import Mkdir
from reemote.produce_grid import produce_grid
from reemote.produce_json import produce_json
from reemote.produce_table import produce_table
from reemote.execute import execute

from typing import List, Tuple, Dict, Any

def inventory() -> List[Tuple[Dict[str, Any], Dict[str, str]]]:
    return [
        (
            {
                'host': '192.168.122.47',  # alpine
                'username': 'youruser',  # User name
                'password': 'yourpassword'  # Password
            },
            {
                'su_user': 'root',
                'su_password': 'rootpassword'  # Password
            }
        ),
        (
            {
                'host': '192.168.122.24',  # alpine
                'username': 'youruser',  # User name
                'password': 'yourpassword'  # Password
            },
            {
                'su_user': 'root',
                'su_password': 'rootpassword'  # Password
            }
        )
    ]


class Make_directory:
    def execute(self):
        yield Mkdir(path="/tmp/mydir", present=True, user="kim", su=True)

async def main():
    results = await execute(inventory(), Make_directory())
    json_output = produce_json(results)
    # print(json_output)
    table_output = produce_table(json_output)
    grid_output = produce_grid(json_output)
    print(grid_output)


if __name__ == "__main__":
    asyncio.run(main())
