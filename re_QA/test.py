class Test:
    def __init__(self, arg1, arg2=2, arg3=3, arg4=4):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg4 = arg4
        

test = Test(1, 2, 3, 4)
test2 = Test(1)
test3 = Test(1, 2)
test4 = Test(1, arg4=4)