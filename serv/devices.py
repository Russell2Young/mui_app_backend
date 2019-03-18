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


@devices.route("/bind_toy", methods=["POST"])
def bind_toy():
    info = request.form.to_dict()
    """
    info = {
        toy_name:toy_name,
        baby_name:baby_name,
        remark:remark,
        device_key : Sdata.device_key,
        user_id:window.localStorage.getItem("user_id")
    }
    """
    # 谁来绑定
    user_info = MONGO_DB.user.find_one({"_id":ObjectId(info.get("user_id"))})

    # 由设备创建玩具
    # // 玩具的名字 √
    # // 伙伴名字 主人名字 √
    # // 谁跟谁绑定 ？ window.localStorage.getItem("user_id")
    # // 主人对用户的称呼 √
    # // 玩具好友列表 ？
    # // 头像 ？

    # 创建app与玩具之间聊天的对话窗口
    chat_window = MONGO_DB.chats.insert_one({"user_list": [], "chat_list": []})

    # 填写玩具基本信息
    toy_info = {
        "device_key": info.get("device_key"),
        "toy_name": info.get("toy_name"),
        "baby_name": info.get("baby_name"),
        "bind_user": info.get("user_id"),
        "avatar": "dash_robot.jpg",
        "friend_list": []
    }

    # 创建玩具的第一个好友 - app user
    toy_first_friend = {
        "friend_id": info.get("user_id"),
        "friend_nick": user_info.get("nickname"),
        "friend_remark": info.get("remark"),
        "friend_avatar": user_info.get("avatar"),
        "friend_chat": str(chat_window.inserted_id),
        "friend_type": "app"
    }

    # 将好友信息追加到 玩具基本信息中
    toy_info["friend_list"].append(toy_first_friend)

    toy = MONGO_DB.toys.insert_one(toy_info)
    # 以上就是创建玩具的过程

    # 给App创建好友 - 玩具
    user_add_friend = {
        "friend_id": str(toy.inserted_id),
        "friend_nick": toy_info.get("toy_name"),
        "friend_remark": toy_info.get("baby_name"),
        "friend_avatar": toy_info.get("avatar"),
        "friend_chat": str(chat_window.inserted_id),
        "friend_type": "toy"
    }

    # 增加app用户的好友
    if user_info.get("friend_list"):
        user_info["friend_list"].append(user_add_friend)
    else:
        user_info["friend_list"] = [user_add_friend]

    # APP用户增加玩具绑定信息
    if user_info.get("bind_toy"):
        user_info["bind_toy"].append(str(toy.inserted_id))
    else:
        user_info["bind_toy"] = [str(toy.inserted_id)]

    # 修改用户数据库中的数据
    MONGO_DB.user.update_one({"_id": user_info.get("_id")}, {"$set": user_info})
    # MONGO_DB.user.update_one({"_id":user_info.get("_id")},{"$push":{"friend_list":user_add_firend}})

    # 聊天窗口信息绑定
    MONGO_DB.chats.update_one({"_id": chat_window.inserted_id},
                              {"$set": {
                                  "user_list": [str(user_info.get("_id")), str(toy.inserted_id)]
                              }
                              }
                              )

    RET["code"] = 0
    RET["msg"] = "玩具绑定成功"
    RET["data"] = {}
    return jsonify(RET)


@devices.route("/toy_list", methods=["POST"])
def toy_list():
    _id = request.form.get("_id")
    # 查询用户已经绑定的玩具
    # 1.先查用户再查玩具
    # 2.查玩具的bind_user
    res_list = list(MONGO_DB.toys.find({"bind_user": _id}))

    for index, item in enumerate(res_list):
        res_list[index]["_id"] = str(item.get("_id"))

    RET["code"] = 0
    RET["msg"] = "查询绑定玩具列表"
    RET["data"] = res_list

    return jsonify(RET)

