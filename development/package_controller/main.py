import re
import json
from nicegui import ui, native, app
from gui.gui import Gui
from reemote.execute import execute
from reemote.produce_grid import produce_grid
from reemote.produce_json import produce_json
from reemote.operations.server.shell import Shell

from reemote.operations.apk.packages import Packages as ApkPackages
from reemote.operations.apt.packages import Packages as AptPackages
from reemote.operations.pip.packages import Packages as PipPackages
from reemote.operations.dpkg.packages import Packages as DpkgPackages
from reemote.operations.dnf.packages import Packages as DnfPackages
from reemote.operations.yum.packages import Packages as YumPackages


class Version_grid:
    def __init__(self):
        app.storage.user["columnDefs1"] = []
        app.storage.user["rowData1"] = []

    def split_package_name_version(self,pkg_str):
        import re
        # Match from end: <version>-r<number>
        # We want to split at the LAST hyphen before "-r<number>"
        parts = pkg_str.rsplit('-', 2)  # Split into at most 3 parts, from the right
        if len(parts) == 3 and re.match(r'^r\d+$', parts[2]):
            name = parts[0]
            version = parts[1] + '-' + parts[2]
            return name, version
        else:
            # Fallback: if format doesn't match, return whole string as name, empty version
            return pkg_str, ""

    async def List_apk_versions(self, responses):
        # Parse packages for each host
        host_packages = []
        host_names = []

        for i, r in enumerate(responses):
            host_name = r.host
            host_names.append(host_name)
            pkgs = r.cp.stdout.splitlines()
            pkg_dict = {}
            for pkg in pkgs:
                name, version = self.split_package_name_version(pkg)
                pkg_dict[name] = version
            host_packages.append(pkg_dict)

        # Get all unique package names across all hosts
        all_package_names = set()
        for pkg_dict in host_packages:
            all_package_names.update(pkg_dict.keys())
        all_package_names = sorted(all_package_names)

        # Build column definitions: Name + one per host
        columnDefs = [{"headerName": "Package Name", "field": "name", 'filter': 'agTextColumnFilter', 'floatingFilter': True}]
        for host_name in host_names:
            columnDefs.append({"headerName": host_name, "field": host_name.replace(".","_")})

        # Build row data
        rowData = []
        for pkg_name in all_package_names:
            row = {"name": pkg_name}
            for i, host_name in enumerate(host_names):
                row[host_name.replace(".","_")] = host_packages[i].get(pkg_name, "")  # empty if not installed
            rowData.append(row)

        # Store in app.storage
        app.storage.user["columnDefs1"] = columnDefs
        app.storage.user["rowData1"] = rowData
        self.version_report.refresh()

    async def List_pip_versions(self, responses):
        host_packages = []
        host_names = []

        for i, r in enumerate(responses):
            host_name = r.host
            host_names.append(host_name)
            data = json.loads(r.cp.stdout)
            row = [{"name": pkg["name"], "version": pkg["version"]} for pkg in data]
            pkg_dict = {}
            for item in row:
                name, version = item["name"], item["version"]
                pkg_dict[name] = version
            host_packages.append(pkg_dict)

        # Get all unique package names across all hosts
        all_package_names = set()
        for pkg_dict in host_packages:
            all_package_names.update(pkg_dict.keys())
        all_package_names = sorted(all_package_names)

        # Build column definitions: Name + one per host
        columnDefs = [{"headerName": "Package Name", "field": "name", 'filter': 'agTextColumnFilter', 'floatingFilter': True}]
        for host_name in host_names:
            columnDefs.append({"headerName": host_name, "field": host_name.replace(".","_")})

        # Build row data
        rowData = []
        for pkg_name in all_package_names:
            row = {"name": pkg_name}
            for i, host_name in enumerate(host_names):
                row[host_name.replace(".","_")] = host_packages[i].get(pkg_name, "")  # empty if not installed
            rowData.append(row)

        # Store in app.storage
        app.storage.user["columnDefs1"] = columnDefs
        app.storage.user["rowData1"] = rowData
        self.version_report.refresh()

    async def List_apt_versions(self, responses):
        host_packages = []
        host_names = []

        # Regular expression to parse package name and version
        pattern = r'^([^/]+).*?\s([^ ]+)\s.*$'

        for i, r in enumerate(responses):
            host_name = r.host
            host_names.append(host_name)
            packages = []
            # Split by lines and ignore the first two lines
            lines = r.cp.stdout.strip().split('\n')[1:]
            for line in lines:
                match = re.match(pattern, line)
                if match:
                    package_name = match.group(1)
                    version = match.group(2)
                    packages.append((package_name, version))

            pkg_dict = {}
            for name, version in packages:
                pkg_dict[name] = version
            host_packages.append(pkg_dict)
            # print(host_packages)

        # Get all unique package names across all hosts
        all_package_names = set()
        for pkg_dict in host_packages:
            all_package_names.update(pkg_dict.keys())
        all_package_names = sorted(all_package_names)

        # Build column definitions: Name + one per host
        columnDefs = [{"headerName": "Package Name", "field": "name", 'filter': 'agTextColumnFilter', 'floatingFilter': True}]
        for host_name in host_names:
            columnDefs.append({"headerName": host_name, "field": host_name.replace(".", "_")})

        # Build row data
        rowData = []
        for pkg_name in all_package_names:
            row = {"name": pkg_name}
            for i, host_name in enumerate(host_names):
                row[host_name.replace(".", "_")] = host_packages[i].get(pkg_name, "")  # empty if not installed
            rowData.append(row)

        # Store in app.storage
        app.storage.user["columnDefs1"] = columnDefs
        app.storage.user["rowData1"] = rowData
        self.version_report.refresh()

    async def List_dnf_versions(self, responses):
        host_packages = []
        host_names = []

        # Fixed regex: capture package name (non-whitespace), then skip whitespace, then capture version (non-whitespace)
        pattern = r'^(\S+)\s+(\S+)'

        for i, r in enumerate(responses):
            host_name = r.host
            host_names.append(host_name)
            pkg_dict = {}

            lines = r.cp.stdout.strip().split('\n')[1:]  # ← ADJUST THIS IF NEEDED

            for line in lines:
                match = re.match(pattern, line)
                if match:
                    package_name = match.group(1)
                    version = match.group(2)
                    pkg_dict[package_name] = version

            host_packages.append(pkg_dict)

        # Get all unique package names across all hosts
        all_package_names = set()
        for pkg_dict in host_packages:
            all_package_names.update(pkg_dict.keys())
        all_package_names = sorted(all_package_names)

        # Build column definitions: Name + one per host
        columnDefs = [{"headerName": "Package Name", "field": "name", 'filter': 'agTextColumnFilter', 'floatingFilter': True}]
        for host_name in host_names:
            columnDefs.append({"headerName": host_name, "field": host_name.replace(".", "_")})

        # Build row data
        rowData = []
        for pkg_name in all_package_names:
            row = {"name": pkg_name}
            for i, host_name in enumerate(host_names):
                row[host_name.replace(".", "_")] = host_packages[i].get(pkg_name, "")  # empty if not installed
            rowData.append(row)

        # Store in app.storage
        app.storage.user["columnDefs1"] = columnDefs
        app.storage.user["rowData1"] = rowData
        self.version_report.refresh()


    async def List_dpkg_versions(self, responses):
        host_packages = []
        host_names = []

        for i, r in enumerate(responses):
            host_name = r.host
            host_names.append(host_name)
            data = json.loads("[" + r.cp.stdout[:-1] + "]")
            row = [{"name": pkg["name"], "version": pkg["version"]} for pkg in data]
            pkg_dict = {}
            for item in row:
                name, version = item["name"], item["version"]
                pkg_dict[name] = version
            host_packages.append(pkg_dict)

        # Get all unique package names across all hosts
        all_package_names = set()
        for pkg_dict in host_packages:
            all_package_names.update(pkg_dict.keys())
        all_package_names = sorted(all_package_names)

        # Build column definitions: Name + one per host
        columnDefs = [{"headerName": "Package Name", "field": "name", 'filter': 'agTextColumnFilter', 'floatingFilter': True}]
        for host_name in host_names:
            columnDefs.append({"headerName": host_name, "field": host_name.replace(".", "_")})

        # Build row data
        rowData = []
        for pkg_name in all_package_names:
            row = {"name": pkg_name}
            for i, host_name in enumerate(host_names):
                row[host_name.replace(".", "_")] = host_packages[i].get(pkg_name, "")  # empty if not installed
            rowData.append(row)

        # Store in app.storage
        app.storage.user["columnDefs1"] = columnDefs
        app.storage.user["rowData1"] = rowData
        self.version_report.refresh()


    @ui.refreshable
    def version_report(self):
        return ui.aggrid({
            'columnDefs': app.storage.user["columnDefs1"],
            'rowData': app.storage.user["rowData1"],
        }).classes('max-h-80  overflow-y-auto')

class Versions:
    def __init__(self):
        self.columns = []
        self.rows = []

    def get_versions(self, responses):
        host_packages = []
        host_names = []

        for i, r in enumerate(responses):
            # print(r.cp.stdout)
            host_name = r.host
            host_names.append(host_name)
            pkg_dict = {}
            for v in r.cp.stdout:
                pkg_dict[v["name"]] = v["version"]
            host_packages.append(pkg_dict)

        # print(host_packages)
        # print(host_names)

        # Get all unique package names across all hosts
        all_package_names = set()
        for pkg_dict in host_packages:
            all_package_names.update(pkg_dict.keys())
        all_package_names = sorted(all_package_names)
        # print(all_package_names)

        # Build column definitions: Name + one per host
        columnDefs = [
            {"headerName": "Package Name", "field": "name", 'filter': 'agTextColumnFilter', 'floatingFilter': True}]
        for host_name in host_names:
            columnDefs.append({"headerName": host_name, "field": host_name.replace(".", "_")})

        # Build row data
        rowData = []
        for pkg_name in all_package_names:
            row = {"name": pkg_name}
            for i, host_name in enumerate(host_names):
                row[host_name.replace(".", "_")] = host_packages[i].get(pkg_name, "")  # empty if not installed
            rowData.append(row)

        self.columns = columnDefs
        self.rows = rowData

    @ui.refreshable
    def version_report(self):
        return ui.aggrid({
            'columnDefs': self.columns,
            'rowData': self.rows,
        }).classes('max-h-40  overflow-y-auto')

class Manager:
    def __init__(self):
        self.sudo = False
        self.su = False
        self.manager = "apk"
        self.package = ""

async def get_versions(gui, versions, manager):
    if manager.manager=='apk':
        from reemote.facts.apk.get_packages import Get_packages
        responses = await execute(app.storage.user["inventory"]],Get_packages())
        versions.get_versions(responses)
        versions.version_report.refresh()
    if manager.manager=='pip':
        from reemote.facts.pip.get_packages import Get_packages
        responses = await execute(app.storage.user["inventory"]],Get_packages())
        versions.get_versions(responses)
        versions.version_report.refresh()
    if manager.manager=='apt':
        from reemote.facts.apt.get_packages import Get_packages
        responses = await execute(app.storage.user["inventory"]], Get_packages())
        versions.get_versions(responses)
        versions.version_report.refresh()
    if manager.manager=='dpkg':
        from reemote.facts.dpkg.get_packages import Get_packages
        responses = await execute(app.storage.user["inventory"]], Get_packages())
        versions.get_versions(responses)
        versions.version_report.refresh()
    if manager.manager=='dnf':
        from reemote.facts.dnf.get_packages import Get_packages
        responses = await execute(app.storage.user["inventory"]], Get_packages())
        versions.get_versions(responses)
        versions.version_report.refresh()
    if manager.manager=='yum':
        from reemote.facts.yum.get_packages import Get_packages
        responses = await execute(app.storage.user["inventory"]], Get_packages())
        versions.get_versions(responses)
        versions.version_report.refresh()


async def install(gui, versions, manager):
    pkg=manager.package
    if manager.manager=='apk':
        from reemote.operations.apk.packages import Packages
        responses = await execute(app.storage.user["inventory"]],Packages(packages=[pkg],present=True, su=manager.su, sudo=manager.sudo))
    if manager.manager=='pip':
        from reemote.operations.pip.packages import Packages
        responses = await execute(app.storage.user["inventory"]],PipPackages(packages=[pkg],present=True, su=manager.su, sudo=manager.sudo))
    if manager.manager=='apt':
        from reemote.operations.apt.packages import Packages
        responses = await execute(app.storage.user["inventory"]],AptPackages(packages=[pkg],present=True, su=manager.su, sudo=manager.sudo))
    if manager.manager=='dpkg':
        from reemote.operations.dpkg.packages import Packages
        responses = await execute(app.storage.user["inventory"]],DpkgPackages(packages=[pkg],present=True, su=manager.su, sudo=manager.sudo))
    if manager.manager=='dnf':
        from reemote.operations.dnf.packages import Packages
        responses = await execute(app.storage.user["inventory"]],DnfPackages(packages=[pkg],present=True, su=manager.su, sudo=manager.sudo))
    if manager.manager=='yum':
        from reemote.operations.yum.packages import Packages
        responses = await execute(app.storage.user["inventory"]],YumPackages(packages=[pkg],present=True, su=manager.su, sudo=manager.sudo))
    # app.storage.user["columnDefs"],app.storage.user["rowData"] = produce_grid(produce_json(responses))
    gui.execution_report.refresh()
    versions.version_report.refresh()


async def remove(gui, versions ,manager):
    pkg=manager.package
    if manager.manager=='apk':
        from reemote.operations.apk.packages import Packages
        responses = await execute(app.storage.user["inventory"]],ApkPackages(packages=[pkg],present=False, su=manager.su, sudo=manager.sudo))
    if manager.manager=='pip':
        from reemote.operations.pip.packages import Packages
        responses = await execute(app.storage.user["inventory"]],PipPackages(packages=[pkg],present=False, su=manager.su, sudo=manager.sudo))
    if manager.manager=='apt':
        from reemote.operations.apt.packages import Packages
        responses = await execute(app.storage.user["inventory"]],AptPackages(packages=[pkg],present=False, su=manager.su, sudo=manager.sudo))
    if manager.manager=='dpkg':
        from reemote.operations.dpkg.packages import Packages
        responses = await execute(app.storage.user["inventory"]],DpkgPackages(packages=[pkg],present=False, su=manager.su, sudo=manager.sudo))
    if manager.manager=='dnf':
        from reemote.operations.dnf.packages import Packages
        responses = await execute(app.storage.user["inventory"]],DnfPackages(packages=[pkg],present=False, su=manager.su, sudo=manager.sudo))
    if manager.manager=='yum':
        from reemote.operations.yum.packages import Packages
        responses = await execute(app.storage.user["inventory"]],YumPackages(packages=[pkg],present=False, su=manager.su, sudo=manager.sudo))
    # app.storage.user["columnDefs"],app.storage.user["rowData"] = produce_grid(produce_json(responses))
    gui.execution_report.refresh()
    versions.version_report.refresh()


@ui.page('/')
def page():
    gui = Gui()
    # version_grid = Version_grid()
    gui.upload_inventory()
    versions = Versions()
    manager = Manager()
    with ui.row():
        ui.label("Package Manager   ")
        ui.select(['apk','pip','apt','dpkg','dnf', 'yum'],value='apk').bind_value(manager, 'manager')
    ui.button('Show installed packages', on_click=lambda: get_versions(gui, versions, manager))
    with ui.row():
        ui.switch('sudo',value=False).bind_value(manager, 'sudo')
        ui.switch('su',value=False).bind_value(manager, 'su')
        ui.input(label='Package').bind_value(manager, 'package')
        ui.button('Add package', on_click=lambda: install(gui, versions, manager))
        ui.button('Remove package', on_click=lambda: remove(gui, versions, manager))
    # version_grid.version_report()
    gui.execution_report()
    versions.version_report()

ui.run(title="Package Controller", reload=False, port=native.find_open_port(),
   storage_secret='private key to secure the browser session cookie')
