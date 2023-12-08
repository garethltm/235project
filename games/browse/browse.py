from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from games.domainmodel.model import Review, User, Wishlist
import games.browse.services as services
from games.utilities import utilities
import games.adapters.repository as repo

browse = Blueprint('browse', __name__, url_prefix='/browse', static_folder='static', template_folder='templates')


@browse.route('/', methods=['GET'])
def browse_home():
    genres = utilities.getAllGenresSorted(repo.repo_instance)
    title_suggestions = utilities.getAllGames(repo.repo_instance)
    publisher_suggestions = utilities.getPublishers(repo.repo_instance)

    checked_genres = request.args.get('genres', "", type=str).split(',')

    search_type = request.args.get('search', "Title", type=str)
    search_term = request.args.get('searchterm', "", type=str)

    games = services.getGamesByGenres(repo.repo_instance, checked_genres)

    if search_term != "":
        if search_type == "Title":
            games = services.searchGameByTitle(games, search_term)
        elif search_type == "Genre":
            games = services.searchGameByGenre(games, search_term)
        elif search_type == "Publisher":
            games = services.searchGameByPublisher(games, search_term)

    per_page = 10
    total_page = (len(games) // per_page) + 1 if len(games) % per_page != 0 else len(games) // per_page
    page = min(max(request.args.get('page', 1, type=int), 1), total_page)

    paginated_games = utilities.paginateLists(games, page, per_page)

    attributes = []
    if checked_genres != ['']:
        attributes.append("genres=" + "%2C".join(checked_genres))
    if search_type != "":
        attributes.append("search=" + search_type)
    if search_term != "":
        attributes.append("searchterm=" + search_term)

    if page < total_page:
        next_page = "?" + "&".join(attributes) + "&page=" + str(page + 1)
    else:
        next_page = None

    if page > 1:
        prev_page = "?" + "&".join(attributes) + "&page=" + str(page - 1)
    else:
        prev_page = None

    first_page = "?" + "&".join(attributes) + "&page=" + "1"
    last_page = "?" + "&".join(attributes) + "&page=" + str(total_page)

    return render_template('browse/browse.html',
                           genres=genres,
                           checked_genres=checked_genres,
                           search_term=search_term,
                           search=search_type,
                           games=paginated_games,
                           title_suggestions=title_suggestions,
                           publisher_suggestions=publisher_suggestions,
                           page=page,
                           total_page=total_page,
                           first_page=first_page,
                           last_page=last_page,
                           next_page=next_page,
                           prev_page=prev_page)


@browse.route('/details')
def browse_detail():
    game_id = request.args.get('id', 0, type=int)
    game = utilities.getGameById(repo.repo_instance, game_id)

    if game is None:
        return render_template('browse/browse_popup.html',
                               browse_h1="ERROR!",
                               browse_h2="Game Not Found. Please try again.",
                               browse_h3="Press OK to return to the browse menu.",
                               )

    if 'username' in session:
        username = session['username']
        user = utilities.getUser(username, repo.repo_instance)
        wishlist = utilities.get_wishlist(repo.repo_instance, user).list_of_games()
        in_wishlist = utilities.is_game_in_wishlist(repo.repo_instance, user, game)
    else:
        wishlist = []
        in_wishlist = False

    # Retrieve all reviews from the database using the repository
    all_reviews = repo.repo_instance.getAllReviews()

    # Filter reviews for the specific game
    reviews = [review for review in all_reviews if review.game == game]
    reviews = reviews[::-1]

    average_rating = utilities.calculate_average_rating(reviews)
    per_page = 5
    total_page = (len(reviews) // per_page) + 1 if len(reviews) % per_page != 0 else len(reviews) // per_page
    page = min(max(request.args.get('page', 1, type=int), 1), total_page)
    paginated_reviews = utilities.paginateLists(reviews, page, per_page)
    attributes = []
    if page < total_page:
        next_page = "?" + "&".join(attributes) + "&id=" + str(game_id) + "&page=" + str(page + 1)
    else:
        next_page = None

    if page > 1:
        prev_page = "?" + "&".join(attributes) + "&id=" + str(game_id) + "&page=" + str(page - 1)
    else:
        prev_page = None

    first_page = "?" + "&".join(attributes) + "&id=" + str(game_id) + "&page=" + "1"
    last_page = "?" + "&".join(attributes) + "&id=" + str(game_id) + "&page=" + str(total_page)

    return render_template('browse/gameDescription.html',
                           game=game,
                           wishlist=wishlist,
                           in_wishlist=in_wishlist,
                           average_rating=average_rating,
                           page=page,
                           total_page=total_page,
                           first_page=first_page,
                           last_page=last_page,
                           next_page=next_page,
                           prev_page=prev_page,
                           reviews=paginated_reviews)
