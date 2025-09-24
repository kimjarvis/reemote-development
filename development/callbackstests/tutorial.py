class Hello_world:
    def execute(self):
        from reemote.operations.server.shell import Shell
        from reemote.result import Result
        r0 : Results = yield Shell("echo 'Hello'")
        print(r0.cp.stdout)
        r1 : Result = yield Shell("echo 'World!'")
        print(r1.cp.stdout)

class Install_wget:
    def execute(self):
        from reemote.operations.apt.packages import Packages
        from reemote.operations.server.shell import Shell
        r0 = yield Packages(packages=["wget"], present=True, sudo=True)
        r1 = yield Shell("which wget")
        print(r1.cp.stdout)

class Which_wget:
    def execute(self):
        from reemote.operations.server.shell import Shell
        r0 = yield Shell("which wget")
        r0.changed = False

class Get_OS:
    def execute(self):
        from reemote.operations.server.shell import Shell
        import re
        r0 = yield Shell("cat /etc/os-release")
        # Extract OS name and version
        os_name_match = re.search(r'PRETTY_NAME="([^"]+)"', r0.cp.stdout)
        os_version_match = re.search(r'VERSION="([^"]+)"', r0.cp.stdout)

        if os_name_match and os_version_match:
            os_name = os_name_match.group(1).split()[0]  # Extract "Debian" from "Debian GNU/Linux"
            os_version = os_version_match.group(1)       # Extract "13 (trixie)"
            print(f"OS Name: {os_name} {os_version}")
        else:
            print("Failed to extract OS details.")

class Get_OS:
    def execute(self):
        from reemote.operations.server.shell import Shell
        import re
        r0 = yield Shell("cat /etc/os-release")
        # Extract OS name and version
        os_name_match = re.search(r'PRETTY_NAME="([^"]+)"', r0.cp.stdout)
        os_version_match = re.search(r'VERSION="([^"]+)"', r0.cp.stdout)

        if os_name_match and os_version_match:
            os_name = os_name_match.group(1).split()[0]  # Extract "Debian" from "Debian GNU/Linux"
            os_version = os_version_match.group(1)       # Extract "13 (trixie)"
            r0.cp.stdout = f"{os_name} {os_version}"
        else:
            r0.cp.stdout = "Failed to extract OS details."


class Show_OS:
    def execute(self):
        r0 = yield Get_OS()
        print(r0.cp.stdout)


async def callback_function(host_info, global_info, command, cp, caller):
    # print("callback")
    # print(host_info["host"])
    # print(global_info)
    # print(command)
    # print(cp)
    # print(caller)
    # Only execute on the first host in the inventory
    # print(host_info["host"])
    # print(caller.host)
    if host_info["host"] == caller.host:
        print("callback called")


from reemote.operation import Operation

class Demonstrate_callback:
    def __init__(self, host: str=None):
        # print(f"Demonstrate_callback init {host}")
        self.host = host

    def execute(self):
        # print(f"self.host {self.host}")
        r1 = yield Operation(f"callback", local=True, callback=callback_function, caller=self)
        # r1 = yield Callback1(callback_function=callback_function, host=self.host)

class Demonstrate_callback1:

    def execute(self):
        # r0 : Results = yield Shell("echo 'Hello'")
        # print(r0.cp.stdout)
        # r1 = yield Operation(f"{self}",composite=True)
        # r1 = yield Put_file(path="example.txt", text="""example
        # """)
        # print(r1)
        # r2 : Result = yield Shell("echo 'World!'")
        # print(r2.cp.stdout)
        # r1 = yield Operation(f"callback", local=True, callback=callback_function, caller=self)

        # Only execute on the first host in the inventory
        # if host_info["host"] == " 10.156.135.16":
        #     print("hi")

        r=yield Demonstrate_callback(host="10.156.135.16")
        # print(inventory()[0][0]['host'])
        # r = yield Demonstrate_callback(host=inventory()[0][0]['host'])
        # print(r)