import sys
from nicegui import native
from reemote.execute import execute
from reemote.produce_grid import produce_grid
from reemote.produce_output_grid import produce_output_grid
from reemote.produce_json import produce_json
from reemote.verify_source_file_contains_valid_class import verify_source_file_contains_valid_class
from reemote.validate_root_class_name_and_get_root_class import validate_root_class_name_and_get_root_class
from development.deploy_manager.local_file_picker import local_file_picker
from reemote.get_classes_in_source import get_classes_in_source

from nicegui import events, ui

from reemote.validate_inventory_structure import validate_inventory_structure
from reemote.verify_inventory_connect import verify_inventory_connect

class Gui:
    def __init__(self):
        self.columns = [{'headerName': 'Command', 'field': 'command'}]
        self.rows = []
        self.inventory = None

    def set(self, columns, rows):
        self.columns = columns
        self.rows = rows

    async def handle_upload(self, e: events.UploadEventArguments):
        text = e.content.read().decode('utf-8')
        exec(text, globals())
        if not validate_inventory_structure(inventory()):
            ui.notify("Inventory structure is invalid")
            return
        if not await verify_inventory_connect(inventory()):
            ui.notify("Inventory connections are invalid")
            return
        ui.notify("Inventory structure and all hosts connect")
        self.inventory = inventory()

        # Start with the fixed column definition for "Command"
        columnDefs = [{'headerName': 'Command', 'field': 'command'}]

        # Dynamically generate column definitions for each host
        for index, (host_info, _) in enumerate(inventory()):
            host_ip = host_info['host']
            columnDefs.append({'headerName': f'{host_ip} Executed', 'field': f'{host_ip.replace(".","_")}_executed'})
            columnDefs.append({'headerName': f'{host_ip} Changed', 'field': f'{host_ip.replace(".","_")}_changed'})
        self.columns = columnDefs
        self.execution_report.refresh()

    @ui.refreshable
    def execution_report(self):
        return ui.aggrid({
            'columnDefs': self.columns,
            'rowData': self.rows,
        }).classes('max-h-40  overflow-y-auto')

    def upload_inventory(self):
        return ui.upload(label="UPLOAD INVENTORY",
             on_upload=self.handle_upload,  # Handle the file upload
        ).props('accept=.py').classes('max-w-full')


class Stdout_report:
    def __init__(self):
        self.columns = [{'headerName': 'Command', 'field': 'command'}]
        self.rows = []

    def set(self, columns, rows):
        self.columns = columns
        self.rows = rows

    @ui.refreshable
    def execution_report(self):
        return ui.aggrid({
            'columnDefs': self.columns,
            'rowData': self.rows,
        }).classes('max-h-40  overflow-y-auto')

class Sources:
    def __init__(self):
        self.source= "/"
        self._classes = []
        self.deployment = ""

    @ui.refreshable
    def classes(self):
        return ui.select(self._classes).bind_value(self, 'deployment')

    async def pick_file(self) -> None:
        result = await local_file_picker('~', multiple=False)
        ui.notify(f'Uploading file {result}')
        self.source = result[0]
        self._classes = get_classes_in_source(result[0])
        self.classes.refresh()

class Wrapper:

    def __init__(self, command):
        self.command = command

    def execute(self):
        # Execute a shell command on all hosts
        r = yield self.command()
        # The result is available in stdout
        # print(r.cp.stdout)


async def run_the_deploy(gui, stdout, sources):
    if sources.source != "/":
        if sources.source and sources.deployment:
            if not verify_source_file_contains_valid_class(sources.source, sources.deployment):
                sys.exit(1)

        # Verify the source and class
        if sources.source and sources.deployment:
            root_class = validate_root_class_name_and_get_root_class(sources.deployment, sources.source)

        if not root_class:
            print("root class not found")
            sys.exit(1)

        responses = await execute(gui.inventory, Wrapper(root_class))
        c, r =produce_grid(produce_json(responses))
        gui.set(c, r)
        gui.execution_report.refresh()
        c, r =produce_output_grid(produce_json(responses))
        stdout.set(c, r)
        stdout.execution_report.refresh()


@ui.page('/')
def page():
    gui = Gui()
    stdout = Stdout_report()
    sources = Sources()
    gui.upload_inventory()
    ui.button('Upload Source', on_click=lambda: sources.pick_file(), icon='folder')
    sources.classes()
    ui.button('Deploy', on_click=lambda: run_the_deploy(gui, stdout, sources))
    stdout.execution_report()
    gui.execution_report()

ui.run(title="Deployment Manager", reload=False, port=native.find_open_port(),
       storage_secret='private key to secure the browser session cookie')
