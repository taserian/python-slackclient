import os

import omdb
import requests


def imdb_info(input_text):
    message_list = []
    if len(input_text) == 0:
        text = "Command format: imdb <title> [ ## <year> ]"
        message_list.append((text, []))
    else:
        text_l = input_text.split("##")
        if len(text_l) == 1:
            # title only
            om = omdb.title(text_l[0], tomatoes=True)
        else:
            # title and year
            om = omdb.title(text_l[0], year=text_l[1], tomatoes=True)

        if "title" in om.keys():
            message_list = output_movie(input_text, om)
        else:
            text = "Sorry, I can't seem to find anything for " + input_text
            message_list.append((text, []))
    return message_list


def imdb_by_code(input_text):
    message_list = []
    if len(input_text) == 0:
        text = "Command format: imdbtt  <imdb_id>"
        message_list.append((text, []))
    else:
        om = omdb.imdbid(input_text, tomatoes=True)
        if "title" in om.keys():
            message_list = output_movie(input_text, om)
        else:
            text = "Sorry, " + input_text + " doesn't seem to be valid."
            message_list.append((text, []))
    return message_list


def output_movie(input_text, om):
    OMDB_API = os.environ.get("OMDB_API")
    output = []
    text = 'This is what I found for "' + input_text + '":'
    attach = list([dict(title=om.title,
                        title_link="http://www.imdb.com/title/" + om.imdb_id,
                        thumb_url="http://img.omdbapi.com/?apikey=" + OMDB_API + "&i=" + om.imdb_id,
                        text=om.plot,
                        fields=list([dict(title="Released", value=om.released, short=True),
                                     dict(title="Runtime", value=om.runtime, short=True),
                                     dict(title="Actors", value=om.actors, short=True),
                                     dict(title="Rating", value=format_rating(om),
                                          short=True)
                                     ])
                        )
                   ])
    output.append((text, attach))
    text = "".join(["<", get_trailer(om.imdb_id), ">"])
    output.append((text, []))
    return output


def get_trailer(imdb_id):
    TMDB_API = os.environ.get("TMDB_API")
    find_movie_url = 'https://api.themoviedb.org/3/find/{id}?api_key={api}&language=en-US&external_source=imdb_id'. \
        format(id=imdb_id, api=TMDB_API)
    t = _GET(find_movie_url)
    if t["movie_results"]:
        tmdb_movie_id = t['movie_results'][0]['id']
        get_trailer_url = 'https://api.themoviedb.org/3/movie/{id}/videos?api_key={api}&language=en-US'.format(
            id=tmdb_movie_id, api=TMDB_API)
        t = _GET(get_trailer_url)
        if t['results']:
            latest_trailer_key = t['results'][0]['key']
            return "http://www.youtube.com/watch?v={yt_key}".format(yt_key=latest_trailer_key)
    else:
        return "No trailer found."


def _GET(path):
    return _request('GET', path)


def _request(method, path):
    response = requests.request(method, path)
    response.raise_for_status()
    response.encoding = 'utf-8'
    return response.json()


def format_rating(item):
    if item.imdb_rating == "N/A":
        imdb_portion = "N/A "
    else:
        imdb_portion = "IMDB: " + item.imdb_rating + "/10 (" + item.imdb_votes + ") "

    if "tomato_meter" in item.keys():
        tomato_portion = "\nTomato: " + item.tomato_meter + "% (" + item.tomato_reviews + ")"
    else:
        tomato_portion = ""

    return imdb_portion + tomato_portion


def imdb_search(input_text):
    OMDB_API = os.environ.get("OMDB_API")
    message_list = []
    if len(input_text) == 0:
        text = "Command format: imdbs <title> [ ## <page> ]"
        message_list.append((text, []))
    else:
        options_list = input_text.split("##")
        # print options_list
        if len(options_list) > 1:
            om = omdb.search(options_list[0], page=options_list[1].strip())
        else:
            om = omdb.search(input_text)
        mn = min(len(om), 10)
        text = "Here's what I found: "
        attach = []
        d = dict()
        for i in range(mn):
            item = om[i]
            d["title"] = (d["title"] if "title" in d.keys() else "") + item.title + " (" + item.year + ") \n"
        attach.append(d)
        message_list.append((text, attach))
    return message_list
