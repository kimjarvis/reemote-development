from nicegui import ui, native, app

grid = ui.aggrid({
    'defaultColDef': {'flex': 1},
    'columnDefs': [{'headerName': 'Command', 'field': 'command'}, {'headerName': 'Name', 'field': 'name'}, {'headerName': '192.168.122.24 Changed', 'field': '192'}, {'headerName': '192.168.122.47 Executed', 'field': 'f19.216812247executed'}, {'headerName': '192.168.122.47\nChanged', 'field': '192.168.122.47_changed'}],
    'rowData': [{'command': "composite Directory(path='/tmp/mydir', present=True, user=None, group=None, guard=True, sudo=False, su=True)",
                 'name': "alice", '192': True, 'f19.216812247executed': True, '192.168.122.47_changed': False}],
    'rowSelection': 'multiple',
}).classes('max-h-40')

def update():
    grid.options['rowData'][0]['age'] += 1
    grid.update()

ui.button('Update', on_click=update)
ui.button('Select all', on_click=lambda: grid.run_grid_method('selectAll'))
ui.button('Show parent', on_click=lambda: grid.run_grid_method('setColumnsVisible', ['parent'], True))

ui.run(title="Manage directory", reload=False, port=native.find_open_port(),
       storage_secret='private key to secure the browser session cookie')
