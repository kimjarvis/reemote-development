

from reemote.operation import Operation


def pre_order_generator(node):
    """
    Enhanced generator function with better error handling and string wrapping.
    """
    stack = [(node, iter(node.execute()))]
    result = None

    while stack:
        current_node, iterator = stack[-1]
        try:
            value = iterator.send(result) if result is not None else next(iterator)
            result = None

            if isinstance(value, tuple):
                # Check if the operation is guarded
                if len(value) == 2 and isinstance(value[0], bool) and isinstance(value[1], str):
                    operation = Operation(value[1],value[0])
                    result = yield operation
                else:
                    raise TypeError(f"Unsupported yield type: {type(value)} {len(value)} {value}")

            # Handle different types of yielded values
            elif isinstance(value, Operation):
                result = yield value
            elif isinstance(value, str):
                # Auto-wrap strings in Operation objects
                operation = Operation(value)
                result = yield operation
            elif hasattr(value, 'execute') and callable(value.execute):
                # If it's a node with execute method, push to stack
                stack.append((value, iter(value.execute())))
            else:
                raise TypeError(f"Unsupported yield type: {type(value)}")

        except StopIteration:
            stack.pop()
        except Exception as e:
            # Handle errors in node execution
            print(f"Error in node execution: {e}")
            stack.pop()




import asyncssh
from asyncssh import SSHCompletedProcess
from reemote.result import Result


async def run_command_on_host(operation):
    # Define the asynchronous function to connect to a host and run a command
    host_info = operation.host_info
    global_info = operation.global_info
    command = operation.command
    cp = SSHCompletedProcess()
    executed = False
    try:
        # Connect to the host
        async with asyncssh.connect(**host_info) as conn:
            if command.startswith("composite"):
                # print(f"Executing composite command: {command}")
                pass
            else:
                if not operation.guard:
                    pass
                else:
                    # print(f"Executing command: {command}")
                    executed = True
                    if command.startswith("sudo"):
                        if not global_info.get("sudo_password"):
                            raise ValueError("Command requires sudo, but no sudo password was provided.")

                        # Construct the full command for sudo
                        full_command = f'echo "{global_info["sudo_password"]}" | sudo -S {command[len("sudo "):]}'

                        # Run the command
                        cp = await conn.run(full_command, check=False)
                    elif command.startswith("su"):
                        full_command = f'su {global_info["su_user"]} -c {command.replace("su", "")}'
                        async with conn.create_process(full_command,
                        # async with conn.create_process(f'su {global_info["su_user"]} -c "ls -ld /tmp/mydir"',
                                                       term_type='xterm',
                                                       stdin=asyncssh.PIPE, stdout=asyncssh.PIPE,
                                                       stderr=asyncssh.PIPE) as process:
                            # Wait for the password prompt and send the password
                            output = await process.stdout.readuntil('Password:')
                            process.stdin.write(f'{global_info["su_password"]}\n')  # Provide the su password
                            # Read the remaining output and check for errors
                            stdout, stderr = await process.communicate()

                            # if process.exit_status != 0:
                            #     print(stderr, end='', file=sys.stderr)
                            #     print(f'Process exited with status {process.exit_status}', file=sys.stderr)
                            # else:
                            #     print(stdout, end='')

                        cp = SSHCompletedProcess(
                            command=full_command ,  # Command executed
                            exit_status=process.exit_status,                     # Exit status
                            returncode=process.returncode,                       # Return code
                            stdout=stdout,                                       # Standard output
                            stderr=stderr                                        # Standard error
                        )
                    else:
                        cp = await conn.run(command, check=False)

    except asyncssh.ProcessError as exc:
        return f"Process on host {host_info.get("host")} exited with status {exc.exit_status}"
    except (OSError, asyncssh.Error) as e:
        return f"Connection failed on host {host_info.get("host")}: {str(e)}"

    # print(f"Output: {cp.stdout}")
    return Result(cp=cp, host=host_info.get("host"), op=operation, executed=executed)






from reemote.pre_order_generator import pre_order_generator
from reemote.run_command_on_host import run_command_on_host

async def run(inventory, obj):
    operations = []
    responses = []

    roots = []
    inventory_items = []
    for inventory_item in inventory:
        roots.append(obj)
        inventory_items.append(inventory_item)  # Store the inventory item
    # Create generators for step-wise traversal of each tree
    generators = [pre_order_generator(root) for root in roots]
    # Result of the previous operation to send
    results = {gen: None for gen in generators}  # Initialize results as None
    # Perform step-wise traversal
    done = False
    while not done:
        all_done = True

        for gen, inventory_item in zip(generators, inventory_items):
            try:
                # print(f"Sending result to generator: {results[gen]}")
                operation = gen.send(results[gen])
                operation.host_info, operation.global_info = inventory_item
                results[gen] = await run_command_on_host(operation)

                # print(f"Operation: {operation}")
                operations.append(operation)
                # print(f"Result: {results[gen]}")
                responses.append(results[gen])

                all_done = False

            except StopIteration:
                pass
        # If all generators are done, exit the loop
        done = all_done
    return operations, responses




import asyncio
from reemote.execute import execute
from reemote.produce_json import produce_json
from reemote.produce_table import produce_table

from typing import List, Tuple, Dict, Any

def inventory() -> List[Tuple[Dict[str, Any], Dict[str, str]]]:
    return [({'host': '192.168.122.24',
              'username': 'youruser',  # User name
              'password': 'yourpassword'  # Password
              },{})]

class Hello_world:
    def execute(self):
        r = yield "echo hello world"
        r.changed = False

async def main():
    responses = await execute(inventory(), Hello_world())
    print(produce_table(produce_json(responses)))


if __name__ == "__main__":
    asyncio.run(main())

"""
This program runs the command echo hello world on the host 192.168.122.24.  The
Hello_world class contains the echo command to be run on the host.  

I want to be able to define an operation that runs locally in the same way.
"""