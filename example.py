def li_start():
  li2 = []
  li2.append([10, 20])
  li2.append([30, 40])
  return li2

def li_ref():
  # li2 = []
  li2 = li[1]
  print(type(li2))
  print(type(li[1]))
  return li2

li = []
li.append([1, 2])
li.append([3, 4])
liA = li_start()
liB = li_ref()

print(li)
print(liA)
print(liB)

listA = [10, 20, 30, 40]
numA = 14
if numA in listA:
  print("correct")
else :
  print("incorrect")

dicA = {"A":3,"B":2,"C":1}
for key in dicA.keys():
  print(key)
#class Links(links):
#  self.links = links

#class Nodes(nodes):
#  self.nodes = nodes
#linkA = Links([])

# path_list = [[[], []], [[], []], [[], []], []]
path_list = []
path = [[1,2,3], [4,5,6]]
for p in path[0]:
  print(p)
index = 0
print(index++)
