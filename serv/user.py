from flask import Blueprint, jsonify, request
from settings import MONGO_DB
from bson import ObjectId

user = Blueprint("user", __name__)


@user.route("/reg", methods=["POST"])
def reg():
    user_info = request.form.to_dict()
    gender = user_info.get("gender")
    user_info["nickname"] = "妈妈" if gender == "1" else "爸爸"
    user_info["avatar"] = "mama.jpg" if gender == "1" else "baba.jpg"
    MONGO_DB.user.insert_one(user_info)

    return jsonify({"code": 0, "msg": "注册成功"})


@user.route("/login", methods=["POST"])
def login():
    user_info = request.form.to_dict()
    res = MONGO_DB.user.find_one(user_info)
    if res:
        res["_id"] = str(res.get("_id"))
        return jsonify({"code": 1, "msg": "登录成功", "data": res})

    return jsonify({"code": 2, "msg": "登录失败!!!", "data": {}})


@user.route("/auto_login", methods=["POST"])
def auto_ogin():
    _id = request.form.get("_id")
    res = MONGO_DB.user.find_one({"id": ObjectId(_id)}, {"password": 0})
    if res:
        res["_id"] = str(res.get("_id"))
        return jsonify({"code": 1, "msg": "登录成功", "data": res})

    return jsonify({"code": 2, "msg": "登录失败!!!", "data": {}})