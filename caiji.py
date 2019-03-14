import requests, os, time
from uuid import uuid4
from settings import MUSIC, COVER, caiji_HEADER, caiji_URL, MONGO_DB


url = caiji_URL
header = caiji_HEADER

# 必须要加上头信息,不然会报错
res = requests.get(url, headers=header)

res_dict = res.json()
data_dict = res.json().get("data")
# {'uid': 0, 'albumId': 11106118, 'sort': 0, 'pageNum': 1, 'pageSize': 30, 'tracksAudioPlay': [{}], 'hasMore': True}
# print(data_dict.get("tracksAudioPlay"))
data_list = data_dict.get("tracksAudioPlay")

content_list = []

for content in data_list:
    file_name = uuid4()

    name = content.get("trackName")
    music = content.get("src")
    cover = "http:" + content.get('trackCoverPath')

    music_contect = requests.get(music)
    music_path = os.path.join(MUSIC, f"{file_name}.mp3")
    with open(music_path, "wb") as f:
        f.write(music_contect.content)

    cover_content = requests.get(cover)
    cover_path = os.path.join(COVER, f"{file_name}.jpg")
    with open(cover_path, "wb") as f:
        f.write(cover_content.content)

    music_info = {
        "music": f"{file_name}.mp3",
        "cover": f"{file_name}.jpg",
        "title": name
    }

    content_list.append(music_info)
    time.sleep(0.5)

MONGO_DB.content.insert_many(content_list)
