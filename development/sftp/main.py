import asyncio
from reemote.execute import execute
from reemote.produce_json import produce_json
from reemote.produce_table import produce_table
from reemote.operation import Operation

from typing import List, Tuple, Dict, Any

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
                'su_password': 'rootuser'  # Password
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
                'su_password': 'rootuser'  # Password
            }
        )
    ]

class Get:
    def __init__(self,
                 path: str,
                 host: str,
                 sudo: bool = False,
                 su: bool = False):
        self.path: str = path
        self.host: str = host
        self.sudo: bool = sudo
        self.su: bool = su

    def __repr__(self) -> str:
        return (f"Get(path={self.path!r}, "
                f"host={self.host!r}, "
                f"sudo={self.sudo!r}, su={self.su!r})")
    def execute(self):
        r0 = yield Operation("echo hello world", local=True)

        # print(r0)
        # Need the inventory here.
        # The sftp client runs on local ! Its not executed on the remote host.
        # run calls run command on host.  We don't want to do that.
        # We want to run the operation on local.

        #Get connection info for one host
        # for host_info, ssh_info in inventory():
        #     if host_info['host'] == '192.168.122.24':
        #         print(host_info)
        #
        #         import asyncio, asyncssh, sys
        #
        #         async def run_client() -> None:
        #             async with asyncssh.connect(**host_info) as conn:
        #                 async with conn.start_sftp_client() as sftp:
        #                     # await sftp.get('example.txt')
        #                     # Open the remote file and read its contents
        #                     async with sftp.open('example.txt', 'r') as remote_file:
        #                         file_content = await remote_file.read()
        #                         print("File Content:")
        #                         print(file_content)  # Or process the string as needed
        #         try:
        #             asyncio.run(run_client())
        #         except (OSError, asyncssh.Error) as exc:
        #             sys.exit('SFTP operation failed: ' + str(exc))


async def main():
    responses = await execute(inventory(), Get(path="example.txt", host="192.168.122.24"))
    print(produce_table(produce_json(responses)))


if __name__ == "__main__":
    asyncio.run(main())
