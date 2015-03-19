def printnode(node):
   # Print state
   print(80 * str(node.row))
   print()
   for row in node.state:
      print(row)
   print()

   # Print column keys and words
   if not node.columnkeys == None:
      print(80 * "-")
      for i, columnkey in enumerate(node.columnkeys):
         if len(node.columnwords[i]) <= 5:
            print("Columnkey.....%d is: %s -> %s" % (i, columnkey, node.columnwords[i]))
         else:
            print("Columnkey.....%d is: %s -> %s (%d)" % (i, columnkey, node.columnwords[i][0:4] + ["..."], len(node.columnwords[i])))
            
   if not node.charsets == None:
      print(80 * "-")
      for i, charset in enumerate(node.charsets):
         if len(charset) <= 11:
            print("Columncharset.%d is: %s" % (i, list(charset)))
         else:
            print("Columncharset.%d is: %s" % (i, list(charset)[0:10] + ['*']))
      
      print(80 * ".")
      print()

      wordcount = len(node.rowwords)
      wordlist = [ word for word in node.rowwords ]

      if wordcount <= 5:
         print("Possible words: %s" % (wordlist))
      else:
         print("Possible words: %s (%d)" % (wordlist[0:4] + ["..."], wordcount))

      print()
