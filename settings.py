# 目录配置
MUSIC = "Music"
COVER = "Cover"
QRCODE = "QRcode"


# 采集配置
caiji_URL = "https://www.ximalaya.com/revision/play/album?albumId=11106118&pageNum=1"
caiji_HEADER = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}

# MongoDB设置
from pymongo import MongoClient

db_client = MongoClient("118.24.243.44", 27017)
MONGO_DB = db_client["myapp"]


# APP数据传输协议
RET = {
    "code": 0,
    "msg": "",
    "data": {},
}


# 二维码设置
LT_URL = "http://qr.topscan.com/api.php?text=%s"