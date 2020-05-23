#!/usr/bin/env python2.7
import json, sys

def getMetaValue(meta, field):
  try:
    return meta[field]["c"][0]["c"]
  except:
    return None

def readin():
  print("hi")
  jsonText = sys.stdin.read()
  jsonObj = json.loads(jsonText)
  print("hello")
  print(jsonObj)
  meta = jsonObj[0]["unMeta"]
  content = jsonObj[1]

  #print json.dumps(jsonObj, indent=4, separators=(',', ': '))

  #SECTION
  new_content = []
  if "section" in meta:
    header_type = 0
    section = getMetaValue(meta, "section")
    for c in content:
      try:
        if c['t'] == "Header":
          content_header_type = c['c'][0]
          if c['c'][1][0] == section:
            header_type = content_header_type
          elif content_header_type <= header_type:
            header_type = 0
        elif header_type > 0:
          new_content.append(c)
      except:
        pass

    content = new_content

  print(json.dumps([jsonObj[0], content]))

if __name__ == "__main__":
  readin()

