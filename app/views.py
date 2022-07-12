from flask import render_template

from app import app


MAIN_MENU_LIST = [
    {"name" : "main_page", "url" : "/"},
    #{"name" : "all_data", "url" : "/all_data/"},
    #{"name" : "forms", "url" : "/forms/"},
    # {"name" : "main_page", "url" : "index_view"},
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        title = "Main",
        menu = MAIN_MENU_LIST,
        )

