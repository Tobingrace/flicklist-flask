from flask import Flask, request, render_template
from jinja2 import Template
import operator

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
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="/static/style.css">
    </head>
    <body>
        <div class="main">
        <div class="header">
            <h1>FlickList</h1>
        </div>
        <div class="spacer"></div>
"""

page_footer = """
    <script type="text/javascript">
        $(document).ready(function ($) {
        $('li').click(function () {
            var movie = this.textContent

            window.alert("Do you want to cross off " + movie + " from your list?");
            if (confirm("Press ok to cross off " + movie) == true) 
            {
                this.style.textDecoration = this.style.textDecoration == 'line-through' ? 'none' : 'line-through';
            } 
            else 
            {
                txt = "action canceled";
            }
        });
        });
    </script>
    </div>
    </body>
</html>
"""

# a form for adding new movies
add_form = """
<div class="edit">
    <form action="/add" method="post">
    <h2>Edit My Watchlist</h2>
        <div class="editsub">
            <label for="new-movie">
            <br></br>
               <p> I want to add
                <input type="text" id="new-movie" name="new-movie"/>
                to my watchlist.</p>
                <p></p>
            </label>
            <div style="float: right;">
            <input style="font: 'Roboto', sans-serif; font-weight: bold;" type="submit" value="Add It"/>
            </div>
        </div>
    </form>
    </div>
"""

# TODO:
# Create the HTML for the form below so the user can check off a movie from their list
# when they've watched it.
# Name the action for the form '/crossoff' and make its method 'post'.

# a form for crossing off watched movies
crossoff_form = """
<div class="movies">
    <h2>Movies to watch</h2>
    <form action="/crossoff" method="post">
    <div class="moviessub">
        <label for="crossed-off-movie">
            <ul>
                {% for movie in movies %}
                    <li class="hvr-box-shadow-inset">{{ movies[movie] }}</li>
                {% endfor%}
            </ul>
        </label>
    </div>
    </form>
</div>
"""

# TODO:
# Finish filling in the function below so that the user will see a message like:
# "Star Wars has been crossed off your watchlist".
# And create a route above the function definition to receive and handle the request from
# your crossoff_form.


@app.route("/crossoff", methods=['GET', 'POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossed-off-movie']
    
    remove_movies(crossed_off_movie)

    crossed_off_movie_element = "<div class='crossoff'> <strike>" + crossed_off_movie + "</strike>"
    confirmation = crossed_off_movie_element + " has been crossed off your Watchlist.  <form action='/' method='GET'><input style='font-size: large;'type='submit' value='Home'/>"

    content = Template(page_header + "<p>" + confirmation + "</p> </div>" + "<div class='spacer2'></div>" + page_footer)

    complete = render_template(content)

    return complete

# TODO:
# modify the crossoff_form above to use a dropdown (<select>) instead of
# an input text field (<input type="text"/>)

crossoff_form2 = """
<div class="editl">
    <form action="/crossoff" method="post">
    <h2>Movies to watch</h2>
        <div class="editsub">
            <label>
                <br></br>
                <p> I want to cross off
                <select name="crossed-off-movie">
                    {% for movie in movies %}
                        <option style="text-align: right;">{{ movies[movie] }}</option>
                    {% endfor%}
                </select>
                from my watchlist.</p>
                <p></p>
            </label>
            <div style="float: right;">
            <input style="font: 'Roboto', sans-serif; font-weight: bold;" type="submit" value="Cross It Off"/>
            </div>
        </div>
    </form>
</div>
"""


@app.route("/add", methods=['POST'])
def add_movie():
    new_movie = request.form['new-movie']
    if new_movie != '':
        add_movies(new_movie)

    # build response content
    new_movie_element = "<div class='crossoff'> <strong>" + new_movie + "</strong>"
    sentence = new_movie_element + " has been added to your Watchlist! <form action='/' method='GET'><input style='font-size: large;'type='submit' value='Home'/>"
    content = Template(page_header + "<p>" + sentence + "</p> </div>" + "<div class='spacer2'></div>" + page_footer)

    complete = render_template(content)

    return complete


@app.route("/")
def index():
    # edit_header = "<h2>Edit My Watchlist</h2>"

    # build the response string
    content = Template(page_header + "<div class='holding'>" + add_form + crossoff_form2 + "</div>" + crossoff_form + page_footer)

    complete = render_template(content, movies=movies)
    return complete


def add_movies(title):
    name = title

    value = max(sorted(movies))
    print(value)

    movies[value+1] = name

    return


def remove_movies(title):
    name = title
    global movies

    movies = {k: v for k, v in movies.items() if v != name}
    
    return movies

    

app.run()
