from reemote.operation import Operation
from reemote.operations.apk.packages import Packages
from reemote.operations.apk.update import Update
from reemote.operations.apk.upgrade import Upgrade
from reemote.operations.apk.info import Info
from reemote.operations.filesystem.mkdir1 import Mkdir


class Install_vim:
    def execute(self):
        yield Packages(packages=["vim"], present=False, su=True)
        yield Update(su=True)
        yield Packages(packages=["apk add vim=9.1.1566-r0"],repository="http://dl-cdn.alpinelinux.org/alpine/edge/main", present=True, su=True)
        yield Upgrade(su=True)

class Get_vim_info:
    def execute(self):
        rx = yield Info(package="vim")
        # print(rx.cp.stdout)

# This seems to work
class Install_nano:
    def execute(self):
        yield Update(su=True)
        yield Packages(packages=["nano"], present=True, su=True)
        r = yield Operation("which nano")
        assert("nano" in r.cp.stdout)
        yield Packages(packages=["nano"], present=False, su=True)
        r = yield Operation("which nano")
        assert("nano" not in r.cp.stdout)

from reemote.operations.filesystem.get_file import Get_file
from reemote.operations.sftp.chmod import Chmod
from reemote.operations.filesystem.put_file import Put_file

# This one isn't going to work because file is write protected
class Files_sudo:
    def execute(self):
        yield Chmod(path="/etc/sudoers", su=True, options="664")
        # yield Get_file(path="/etc/sudoers",host="192.168.122.24")

# This one does not work but it should
#localhost:~$ nginx: [alert] could not open error log file: open() "/var/lib/nginx/logs/error.log" failed (13: Permission denied)
# 2025/09/14 10:21:41 [warn] 14417#14417: the "user" directive makes sense only if the master process runs with super-user privileges, ignored in /etc/nginx/nginx.conf:3
# 2025/09/14 10:21:41 [emerg] 14417#14417: mkdir() "/var/lib/nginx/tmp/client_body" failed (13: Permission denied)
class Nginx_update:
    def execute(self):
        yield Update(su=True)
        r = yield Packages(packages=["nginx"], present=True, su=True)
        # print(r)
        r1= yield Operation("rc-service nginx start")
        # print(r1)
        r2= yield Operation("su rc-update add nginx")
        # print(r2)
        r3 = yield Chmod(path="/etc/nginx/http.d/",options="o+w",su=True)
        # print(r3)
        r4 = yield Put_file(path="/etc/nginx/http.d/custom.conf",text="""
server {
    listen       80;
    server_name  localhost;

    location / {
        return 200 'Hello from Reemote!\n';
        add_header Content-Type text/plain;
    }
}
        """)
        # print(r4)
        r5= yield Operation("su rc-service nginx reload")
        # print(r5)



class Nginx_serve:
    def execute(self):
        yield Update(su=True)
        r = yield Packages(packages=["nginx"], present=True, su=True)
        # print(r)
        r0 = yield Mkdir(path="/var/www/html", present=True, su=True)
        # print(r0)
        r1 = yield Put_file(path="/var/www/html/index.html", text="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Welcome to Reemote on Alpine Nginx</title>
        </head>
        <body>
            <h1>Hello from Reemote on Alpine Linux with Nginx!</h1>
            <p>Your web server is working correctly.</p>
        </body>
        </html>
        """)
        # print(r1)
        r2 = yield Put_file(path="/etc/nginx/nginx.conf",text="""
        user nginx;
        worker_processes auto;

        events {
            worker_connections 1024;
        }

        http {
            include /etc/nginx/mime.types;
            default_type application/octet-stream;

            sendfile on;
            keepalive_timeout 65;

            server {
                listen 80;
                server_name localhost;

                location / {
                    root /var/www/html;
                    index index.html;
                }
            }
        }
        """)
        # print(r2)
        r3= yield Operation("rc-service nginx start")
        # print(r3)
        r4= yield Operation("su rc-update add nginx")
        # print(r4)
