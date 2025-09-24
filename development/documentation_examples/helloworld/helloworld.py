import asyncio

from reemote.produce_table import produce_table
from reemote.produce_json  import produce_json
from reemote.execute import execute
from reemote.operation import Operation
from typing import List, Tuple, Dict, Any

def inventory() -> List[Tuple[Dict[str, Any], Dict[str, str]]]:
    return [({'host': 'localhost',
              'username': 'youruser',  # User name
              'password': 'yourpassword'  # Password
              },{})]

class Hello_world:
    def execute(self):
        r = yield Operation("echo hello world")
        r.changed = False

async def main():
    results = await execute(inventory(), Hello_world())
    print(produce_table(produce_json(results)))

if __name__ == "__main__":
    asyncio.run(main())
