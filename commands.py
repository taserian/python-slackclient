import os

import omdb


def imdb_info(input_text):
    OMDB_API = os.environ.get("OMDB_API")
    if len(input_text) == 0:
        text = "Command format: imdb <title> [ ## <year> ]"
        attach = []
    else:
        textL = input_text.split("##")
        if len(textL) == 1:
            # title only
            om = omdb.title(textL[0], tomatoes=True)
        else:
            # title and year
            om = omdb.title(textL[0], year=textL[1], tomatoes=True)
        if "title" in om.keys():
            text = 'This is what I found for "' + input_text + '":'
            attach = list([dict(title=om.title,
                                title_link="http://www.imdb.com/title/" + om.imdb_id,
                                thumb_url="http://img.omdbapi.com/?apikey=" + OMDB_API + "&i=" + om.imdb_id,
                                text=om.plot,
                                fields=list([dict(title="Released", value=om.released, short=True),
                                             dict(title="Runtime", value=om.runtime, short=True),
                                             dict(title="Actors", value=om.actors, short=True),
                                             dict(title="Rating", value=format_rating(om),
                                                  short=True)])
                                )])
        else:
            text = "Sorry, I can't seem to find anything for " + input_text
            attach = []
    return text, attach


def format_rating(item):
    imdb_rating = item.imdb_rating
    imdb_votes = item.imdb_votes
    tomato_meter = item.tomato_meter
    if imdb_rating == "N/A":
        imdb_portion = "N/A "
    else:
        imdb_portion = imdb_rating + "/10 (" + imdb_votes + ") "
    tomato_portion = "// Tomato: " + tomato_meter
    return imdb_portion + tomato_portion


def imdb_search(input_text):
    OMDB_API = os.environ.get("OMDB_API")

    if len(input_text) == 0:
        text = "Command format: imdbs <title> [ ## <page> ]"
        attach = []
    else:
        options_list = input_text.split("##")
        if len(options_list) > 1:
            om = omdb.search(options_list[0], page=options_list[1])
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
    return text, attach
