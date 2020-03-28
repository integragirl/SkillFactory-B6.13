import json

from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import b_6_13_album as album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Количество альбомов {}<br>".format(len(albums_list))
        result += "Список альбомов {}:<br> ".format(artist)
        result += "<br>".join(album_names)
    return result


@route("/albums", method="POST")
def user():
    user_data = {
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album"),
        "year": int(request.forms.get("year"))
    }

    if album.find_(user_data).count() > 0:
        result = HTTPError(409, "Данные об этом альбоме уже есть в базе")
    else:
        album.save_album(user_data)
        result = "Данные успешно сохранены"

    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)