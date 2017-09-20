from flask import Flask, request, render_template
from jinja2 import Template

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

movies = {0: 'The Matrix', 1: 'Vanillia Sky',
          2: 'Shawshank Redemption', 3: 'Fight Club',
          4: 'Inception'}

page_header = """
<!DOCTYPE html>
<html>
    <head>
    <meta charset="utf-8">
    <meta name="Movie picks for both today and tomorrow" content="Movies">
    <meta name="Jason Hart" content="Movies">

    <title>FlickList: LC101</title>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <link rel="stylesheet" type="text/css" href="/static/style.css">
    </head>
    <body>
        <h1>FlickList</h1>
"""

page_footer = """
    <script type="text/javascript">
        $(document).ready(function ($) {
        $('li').click(function () {
            this.style.textDecoration = this.style.textDecoration == 'line-through' ? 'none' : 'line-through';
        });
        });
    </script>
    </body>
</html>
"""

# a form for adding new movies
add_form = """
    <form action="/add" method="post">
        <label for="new-movie">
            I want to add
            <input type="text" id="new-movie" name="new-movie"/>
            to my watchlist.
        </label>
        <input type="submit" value="Add It"/>
    </form>
"""

# TODO:
# Create the HTML for the form below so the user can check off a movie from their list
# when they've watched it.
# Name the action for the form '/crossoff' and make its method 'post'.

# a form for crossing off watched movies
crossoff_form = """
    <form action="/add" method="post">
        <label for="crossed-off-movie">
            <h2> Movies to watch</h2>
            <ul>
                {% for movie in movies %}
                    <li class="hvr-box-shadow-inset">{{ movies[movie] }}</li>
                {% endfor%}
            </ul>
        </label>
    </form>
"""

# TODO:
# Finish filling in the function below so that the user will see a message like:
# "Star Wars has been crossed off your watchlist".
# And create a route above the function definition to receive and handle the request from
# your crossoff_form.


@app.route("/crossoff", methods=['POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossoff_form']

    content = crossoff_form

    return content

# TODO:
# modify the crossoff_form above to use a dropdown (<select>) instead of
# an input text field (<input type="text"/>)


@app.route("/add", methods=['POST'])
def add_movie():
    new_movie = request.form['new-movie']

    # build response content
    new_movie_element = "<strong>" + new_movie + "</strong>"
    sentence = new_movie_element + " has been added to your Watchlist!"
    content = page_header + "<p>" + sentence + "</p>" + page_footer

    return content


@app.route("/")
def index():
    edit_header = "<h2>Edit My Watchlist</h2>"

    # build the response string
    content = Template(page_header + edit_header +
                       add_form + crossoff_form + page_footer)

    complete = render_template(content, movies=movies)
    return complete


app.run()
