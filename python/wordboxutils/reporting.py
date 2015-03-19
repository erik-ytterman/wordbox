def printnode(depth, node):
   print("\n" + 80 * str(depth) + "\n")
   for i, row in enumerate(node.state):
      print("%d: %s" % (i, row))

