from flask import Blueprint, jsonify, request
from settings import MONGO_DB, RET
from bson import ObjectId

devices = Blueprint("devices", __name__)


@devices.route("/device_key", methods=["POST"])
def device_key():
    device_dict = request.form.to_dict()
    res = MONGO_DB.devices.find_one(device_dict)
    # device_key是否已经做过绑定了?
    if res:
        RET["msg"] = "扫描成功啦!"
        RET["data"] = device_dict
        return jsonify(RET)
    else:
        RET["code"] = 1
        RET["msg"] = "扫描失败咯~"
        RET["data"] = {}
    return jsonify(RET)