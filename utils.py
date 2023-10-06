import json
import os

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

def createFile(filename):
  f = open(filename, "w+")
  return f

def fileExists(filename):
  return os.path.isfile(filename)