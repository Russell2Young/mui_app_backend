from flask import Flask
from serv import content, get_set_anything, user, devices

app = Flask(__name__)

app.register_blueprint(content.content)
app.register_blueprint(get_set_anything.gsa)
app.register_blueprint(user.user)
app.register_blueprint(devices.devices)

if __name__ == '__main__':
    app.run("0.0.0.0", 9528, debug=True)
