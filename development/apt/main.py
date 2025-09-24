import asyncio
from reemote.execute import execute
from reemote.produce_json import produce_json
from reemote.produce_table import produce_table
from reemote.operations.server.shell import Shell
from reemote.operation import Operation
from reemote.operations.apt.packages import Packages
from reemote.operations.apt.update import Update
from reemote.operations.apt.upgrade import Upgrade
from typing import List, Tuple, Dict, Any

from typing import List, Tuple, Dict, Any

class Hello_world:
    def execute(self):
        # r0 = yield Operation(f"{self}",composite=True)
        # print(r0)
        # r = yield Shell("apt-get install vim",sudo=True)
        # print(r)
        # r = yield Packages(packages=["vim"], present=True, sudo=True)
        r = yield Update(sudo=True)
        # print(r)

class Packages_example:
    def execute(self):
        from reemote.operations.apt.packages import Packages
        from reemote.operations.server.shell import Shell
        # Add the packages on all hosts
        r = yield Packages(packages=["vim"],present=True, sudo=True)
        # Verify installation
        r = yield Shell("which vim")
        # print(r.cp.stdout)
        # Delete the packages on all hosts
        r = yield Packages(packages=["vim"],present=False, sudo=True)
        # Verify removal
        r = yield Shell("which vim")
        # print(r.cp.stdout)


    def __repr__(self):
        return (f"Hello_world()")


async def main():
    responses = await execute(inventory(), Hello_world())
    print(produce_table(produce_json(responses)))

if __name__ == "__main__":
    asyncio.run(main())