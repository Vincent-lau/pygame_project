class A(object):
    def __init__(self):
        print("a")

class B(object):
    def __init__(self):
        print('b')

class C(A,B):
    def __init__(self):
        super().__init__()
        A().__init__()



n=C()
