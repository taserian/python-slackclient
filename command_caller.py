import bot_commands as c


def call_imdb_info(i):
    print(c.imdb_info(i))


def call_imdb_by_code(c):
    print(c.imdb_by_code(c))


def call_imdb_search(s):
    print(c.imdb_search(s))


def test_each_output():
    print("imdb Fantastic Four ## 1994")
    call_imdb_info("Fantastic Four ## 1994")
    print("imdb white comanche")
    call_imdb_info("white comanche")
