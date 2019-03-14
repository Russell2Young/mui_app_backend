from flask import Flask, request, jsonify
from mui_settings import db

app = Flask(__name__)


@app.route("/login", methods=["POST", "GET"])
def login():
    print(request)
    print(request.form.to_dict())
    # res = request.form.to_dict()
    # if res.get("msg") == "reg":
    #     db.users.insert_one(res)
    #     return jsonify({"code": 2, "msg": "注册成功"})
    # elif res['username'] == db:
    res = db.users.find_one(request.form.to_dict())
    print(res)
    _id = str(res.get("_id"))
    if res:
        return jsonify({"code": 1, "msg": "登陆成功", "nick": request.form.get("username"), "_id": _id})
        # return jsonify({"code": 1, "msg": "登陆成功", "nick": request.form.get("username")})
    # else:
    #     db.users.insert_one(request.form.to_dict())
    return jsonify({"code": 0, "msg": "用户名密码错误"})


if __name__ == '__main__':
    app.run("0.0.0.0", "9527", debug=True)

