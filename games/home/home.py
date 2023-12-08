from flask import Blueprint, render_template

from games.home import services
from games.utilities import utilities
import games.adapters.repository as repo


home = Blueprint('home', __name__, static_folder='static', template_folder='templates')


@home.route('/', methods=['GET'])
def home_home():
    featuredGames = services.getFeaturedGames(repo.repo_instance)
    genres = utilities.getAllGenresSorted(repo.repo_instance)
    title_suggestions = utilities.getAllGames(repo.repo_instance)
    publisher_suggestions = utilities.getPublishers(repo.repo_instance)



    return render_template('home/home.html',
                           featuredGames=featuredGames,
                           genres=genres,
                           title_suggestions=title_suggestions,
                           publisher_suggestions=publisher_suggestions
                           )
