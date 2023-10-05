import json

def loadJson(filename):
  f = open(filename, "r")
  loadedJson = json.load(f)
  f.close()
  return loadedJson

def saveJson(filename, data):
  f = open(filename, "w+")
  formattedData = json.dumps(data)
  f.write(formattedData)
  f.close()