from flask import Blueprint, jsonify, send_file
from settings import MONGO_DB, COVER, MUSIC
import os

gsa = Blueprint("gsa", __name__)


@gsa.route("/get_image/<filename>")
def get_image(filename):
    file_path = os.path.join(COVER, filename)

    return send_file(file_path)


@gsa.route("/get_music/<filename>")
def get_music(filename):
    file_path = os.path.join(MUSIC, filename)

    return send_file(file_path)
