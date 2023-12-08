from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from games.authentication.authentication import login_required
from games.domainmodel.model import User, Wishlist
import games.wishlist.services as wishlist_services
from games.utilities.utilities import getUser, getGameById, get_wishlist
import games.adapters.repository as repo
from flask import jsonify

wishlist = Blueprint('wishlist', __name__, url_prefix='/wishlist', static_folder='static', template_folder='templates')

@wishlist.route('/', methods=['GET'])
@login_required
def view_wishlist():
    if 'username' not in session:
        flash("Please log in to submit a review.", "error")
        return redirect(url_for('authentication.login'))
    username = session['username']
    user = getUser(username, repo.repo_instance)

    wishlist = get_wishlist(repo.repo_instance, user)
    return render_template('wishlist/wishlist.html',
                           wishlist=wishlist.list_of_games())


@wishlist.route('/add_to_wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    # if 'username' not in session:
    #     flash("Please log in to submit a review.", "error")
    #     return redirect(url_for('authentication.login'))
    username = session['username']
    user = getUser(username, repo.repo_instance)
    # user = User("AaronChiam", "password")  # default to aaron for now
    game_id = int(request.form['game_id'])

    game = getGameById(repo.repo_instance, game_id)
    if game is not None:
        wishlist = get_wishlist(repo.repo_instance, user)
        if not wishlist:
            wishlist = Wishlist(user)
        
        if game not in wishlist.list_of_games():
            wishlist.add_game(game)
        
        wishlist_services.add_wishlist(repo.repo_instance, user, wishlist)

    return jsonify({'result': 'success'})


@wishlist.route('/remove', methods=['POST'])
@login_required
def remove_wishlist():
    # if 'username' not in session:
    #     flash("Please log in to submit a review.", "error")
    #     return redirect(url_for('authentication.login'))
    username = session['username']
    user = getUser(username, repo.repo_instance)
    # user = User("AaronChiam", "password")  # default to aaron for now
    game_id = request.form.get('game_id')
    
    game = getGameById(repo.repo_instance, int(game_id))
    print(game)
    if game is not None:

        wishlist_services.remove_game_from_wishlist(repo.repo_instance, user, game)

        wishlist = get_wishlist(repo.repo_instance, user)
        print(wishlist.list_of_games())
        
    return jsonify({'result': 'success'})
