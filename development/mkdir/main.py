import asyncssh
from reemote.commands.sftp.mkdir import Mkdir
from reemote.commands.sftp.write_file import Write_file
from reemote.operations.server.shell import Shell
from reemote.operations.users.add_user import Add_user
from reemote.operations.users.add_sudo_user import Add_sudo_user

class Test_Mkdir():
    def execute(self):

        # # Create a file from text with default permissions
        # r = yield Write_file(path='example.txt', text='Hello World!')
        #
        # # Create a file with specific permissions
        # r = yield Write_file(
        #     path='script.sh',
        #     text='#!/bin/bash\necho "Hello World"',
        #     attrs=asyncssh.SFTPAttrs(permissions=0o755)
        # )
        #
        # # Create a file with owner and timestamps
        # r = yield Write_file(
        #     path='config.json',
        #     text='{"key": "value"}',
        #     attrs=asyncssh.SFTPAttrs(
        #         permissions=0o644,
        #         uid=1000,
        #         gid=1000,
        #         mtime=1672531200
        #     )
        # )
        #
        # # Verify the file content
        # r = yield Shell("cat example.txt")
        # print(r.cp.stdout)
        #
        # yield Mkdir(
        #     path='/etc/sudoers.d',
        #     attrs=asyncssh.SFTPAttrs(
        #         permissions=0o755,
        #     )
        # )
        #
        # # Sudo Configuration
        # yield Write_file1(
        #     path='/etc/sudoers.d/kim',
        #     text='kim ALL=(ALL) NOPASSWD:ALL',
        #     attrs = asyncssh.SFTPAttrs(
        #         mode= '0440',
        #         owner='root',
        #         group='root',
        #     ),
        #     sudo=True
        # )
        #
        # # Write to a temporary location first
        # yield Write_file(
        #     path='/tmp/kim',
        #     text='kim ALL=(ALL) NOPASSWD:ALL',
        #     attrs=asyncssh.SFTPAttrs(permissions=0o444)
        # )
        #
        # # Move with sudo
        # yield Shell(
        #     'sudo mv /tmp/kim /etc/sudoers.d/kim',
        #     sudo=True
        # )
        #
        # # Set final permissions
        # yield Shell(
        #     'sudo chmod 0440 /etc/sudoers.d/kim && sudo chown root:root /etc/sudoers.d/kim',
        #     sudo=True
        # )

        yield Add_user(user="alice", password="passwd")
        yield Add_sudo_user(user="alice", password="passwd")