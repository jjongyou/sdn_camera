def add(one = 1, two = 2, three = 3):
  if two is None:
    return one + three
  else:
    return one + two + three
"""
def effect(num1, num2 = None, num3):
  if num2 is None:
    return num1 + num3
  else :
    return num1 + num2 + num3
"""
print("3 params")
print(add(1, 2, 3))
print("2 param")
print(add(1, 2))

"""
print("3 parameters")
print(effect(1, 2, 3))
print("2 parameters")
print(effect(1, 2))
"""
