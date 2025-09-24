class Shell_example:
    def execute(self):
        from reemote.operations.server.shell import Shell
        # Execute a shell command on all hosts
        r = yield Shell("echo Hello World")
        # The result is available in stdout
        print(r.cp.stdout)

class Info_example:
    def execute(self):
        from reemote.operations.apk.info import Info
        # Get the package information on all hosts
        r = yield Info(package='vim')


class Get_os_example:
    def execute(self):
        from reemote.facts.server.get_os import Get_OS
        r = yield Get_OS("NAME")
