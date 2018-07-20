import json
from xml.dom.minidom import Document

src = open('/home/lianji/MC_data/train_data/example/00002150_all_videos_robot2_03_mp4.jpg.json')
obj = json.loads(src.read())

print obj
print len(obj['Rects'])
print obj['Hardscene']