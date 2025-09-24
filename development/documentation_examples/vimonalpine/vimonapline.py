import asyncio
from reemote.execute import execute

from reemote.operations.apk.packages import Packages
from reemote.operations.apk.update import Update
from reemote.produce_table import produce_table
from reemote.produce_json import produce_json
from reemote.operation import Operation
from typing import List, Tuple, Dict, Any


def inventory() -> List[Tuple[Dict[str, Any], Dict[str, str]]]:
    return [({'host': '192.168.122.47',
              'username': 'youruser',  # User name
              'password': 'yourpassword'  # Password
              }, {
                 'su_user': 'youruser',
                 'su_password': 'yourpassword'})]


class Install_vim:
    def execute(self):
        r = yield Operation("echo Installing VIM on Alpine!")
        r.changed = False
        yield Update(su=True)
        yield Packages(packages=["vim"], present=True, su=True)


async def main():
    results = await execute(inventory(), Install_vim())
    print(produce_table(produce_json(results)))


if __name__ == "__main__":
    asyncio.run(main())
