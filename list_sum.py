start = "fl"
lists = ["fr", "rl", "rr"]

links = lists
links.insert(0, start)
nodes = ["A", "B", "C", "D"]

for node, link in zip(nodes, links):
  print(node, link)
