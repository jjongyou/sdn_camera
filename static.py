class Node():
  count = 3
  def __init__(self, name):
    self.name = name

  def get(self):
    return self.name, self.count


node = Node("fuck")
print(node.get())
