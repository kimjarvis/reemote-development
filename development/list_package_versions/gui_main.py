from nicegui import ui, native, app
from gui.gui import Gui
from reemote.execute import execute
from reemote.produce_grid import produce_grid
from reemote.produce_json import produce_json
from reemote.operations.server.shell import Shell

def split_package_name_version(pkg_str):
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

class Gui1:
    def __init__(self):
        app.storage.user["columnDefs1"] = [{"headerName": "Name", "field": "name"},{"headerName": "Version", "field": "version"}]
        app.storage.user["rowData1"] = []

    async def List_package_versions(self,responses):
            r = responses[0]
            result = [split_package_name_version(pkg) for pkg in r.cp.stdout.splitlines()]
            rows=[]
            for name, version in result:
                rows.append({"name": name, "version": version})
            app.storage.user["rowData1"] = rows
            self.version_report.refresh()

    @ui.refreshable
    def version_report(self):
        return ui.aggrid({
            'columnDefs': app.storage.user["columnDefs1"],
            'rowData': app.storage.user["rowData1"],
        }).classes('max-h-40  overflow-y-auto')


async def Control_directory(gui,gui1):
    responses = await execute(app.storage.user["inventory"],Shell("apk info -v"))
    await gui1.List_package_versions(responses)
    app.storage.user["columnDefs"],app.storage.user["rowData"] = produce_grid(produce_json(responses))
    gui.execution_report.refresh()
    gui1.version_report.refresh()

@ui.page('/')
def page():
    gui = Gui()
    gui1 = Gui1()
    gui.upload_inventory()
    ui.button('Run', on_click=lambda: Control_directory(gui,gui1))
    gui1.version_report()
    gui.execution_report()


ui.run(title="Manage directory", reload=False, port=native.find_open_port(),
       storage_secret='private key to secure the browser session cookie')
