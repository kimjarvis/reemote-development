from reemote.operations.sftp.touch import Touch
from reemote.operations.sftp.chmod import Chmod

class Touch_freddy:
    def execute(self):
        yield Touch(path="/home/kim/freddy", present=True, su=True)
        yield Chmod(path="/home/kim/freddy", options="+x", su=True)
