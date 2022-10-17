import yaml
class Node():
  def __init__(self, ip_to_port, link_to_port, dpid):
    self.ip_to_port = ip_to_port
    self.link_to_port = link_to_port
    self.dpid = dpid
    self.name = name
  
class Path():
  def __init__(self, links, nodes):
    self.links = links
    self.nodes = nodes

with open("../network_info.yaml") as yaml_file:
  network_info = yaml.load(yaml_file, Loader=yaml.FullLoader)
"""
print(type(network_info))

print("========")
print("ip_to_port")
print(network_info["ip_to_port"])
print("link_to_port")
print(network_info["link_to_port"])
print("dpid")
print(network_info["dpid"])
print("host_to_switch")
print(network_info["host_to_switch"])
print("route_table")
print(network_info["route_table"])
print("bandwidth_table")
print(network_info["bandwidth_table"])


print("======= route_table None ========")
print(network_info["route_table"]["fr"]["fl"])
print(type(network_info["route_table"]["fr"]["fl"]))

if network_info["route_table"]["fr"]["fl"] is None:
  print("This is None")
else :
  print("It is not None")
"""
# ===================================================
rte_tbl = {}
rte_tbl.setdefault("route_table", {})
links = []
nodes = []
print("===========START============")
for src_node in network_info["route_table"].keys():
  rte_tbl["route_table"].setdefault(src_node, {})

  for dst_node in network_info["route_table"][src_node].keys():
    rte_tbl["route_table"][src_node].setdefault(dst_node, {})

    if network_info["route_table"][src_node][dst_node] is not None:
      for paths in network_info["route_table"][src_node][dst_node].values():
        rte_tbl["route_table"][src_node][dst_node] = []

        for path in paths:
          # for key, value in path:
          print("=== PATH ===")
          print(path["links"])
          print(path["nodes"])
          # sdn_path = Path(path["links"], path["nodes"])
          sdn_path = Path(path["links"], path["nodes"])
          rte_tbl["route_table"][src_node][dst_node].append(sdn_path)

print("===========END============")

print(rte_tbl)
print(len(rte_tbl["route_table"]["fl"]["fr"]))
