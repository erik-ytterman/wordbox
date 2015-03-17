def loadwords(columns, filename = r'../swedish-word-list.txt'):
   normalizer = lambda line: line.strip().upper()
   worddata = [ normalizer(word) for word in open(filename, encoding="ISO-8859-1") ]
   wordset = { word for word in sorted(worddata) if len(word) == columns }
   
   return wordset
