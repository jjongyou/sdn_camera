li = [{"links": ["A", "B"], "nodes": ["APPLE", "BANANA"]}]
print(li)

print(type(li))
for a in li:
  print(type(a))
  print(a)
  print(a["links"])
  print(a["nodes"])
"""
  for b in a:
    print(type(b))
    print(b)
    print("==START==")
    print(a[b])
"""
