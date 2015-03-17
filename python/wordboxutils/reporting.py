def printnode(node):
   # Print state
   print(30 * str(node.row))
   for row in node.state:
      print(row)
      
   # Print column keys and words
   if not node.columnkeys == None:
      print(30 * "-")
      for i, columnkey in enumerate(node.columnkeys):
         if len(node.columnwords[i]) <= 7:
            print("Key for column: %d is %s -> %s" % (i, columnkey, node.columnwords[i]))
         else:
            print("Key for column: %d is %s -> %s" % (i, columnkey, "MANY"))
            
   if not node.charsets == None:
      print(30 * "+")
      for i, charset in enumerate(node.charsets):
         print("Charset for column: %d is %s" % (i, charset))
      if len(node.rowwords) <= 7:
         print("Possible words: %s" % (node.rowwords))
      else:
         print("Possible words: %s" % ("MANY"))

   print(30 * str(node.row))
