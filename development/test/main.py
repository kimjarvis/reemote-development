from development.callbackstests.test import Test

class Test_su:
    def execute(self):
        r = yield Test(package="vim", su=True)
        # print(r.cp.stdout)
