import math
from Ma3yTuKserializer.serializers.json_serializer import Json
from Ma3yTuKserializer.serializers.xml_serializer import Xml


def my_decor(meth):
    def inner(*args, **kwargs):
        print('I am in my_decor')
        return meth(*args, **kwargs)

    return inner


class A:
    x = 10

    @my_decor
    def my_sin(self, c):
        return math.sin(c * self.x)

    @staticmethod
    def stat():
        return 145

    def __str__(self):
        return 'AAAAA'

    def __repr__(self):
        return 'AAAAA'


class B:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def prop(self):
        return self.a * self.b

    @classmethod
    def class_meth(cls):
        return math.pi


class C(A, B):
    pass


ser = Json()

# var = 15
# var_ser = ser.dumps(var)
# var_des = ser.loads(var_ser)
# print(var_des)

C_ser = ser.dumps(C)
C_des = ser.loads(C_ser)

c = C_des(1, 2)
c_ser = ser.dumps(c)
c_des = ser.loads(c_ser)

print(c_des)
print(c_des.x)
print(c_des.my_sin(10))
print(c_des.prop)
print(C_des.stat())
print(c_des.class_meth())

def gen(n):
    a = 2
    for i in range(n):
        a *= a
        yield a

def rec(n):
    if not n:
        return
    return rec(not n)

t = ser.dumps(gen(4))
r = ser.loads(t)
rec = ser.dumps(rec)
rec = ser.loads(rec)

print(next(r))
rec(True)

f = C(1, 2)
print(f.my_sin(11))

def main():
    serializer = Json()
    result = serializer.dumps("Hello")
    print(result)


if __name__ == "__main__":
    main()