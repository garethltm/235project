from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from games.authentication.authentication import login_required
from games.domainmodel.model import Review, User, Wishlist
from games.utilities import utilities
import games.adapters.repository as repo
from sqlalchemy.orm import sessionmaker

review = Blueprint('review', __name__, url_prefix='/review', static_folder='static', template_folder='templates')


@review.route('/submit_review', methods=['GET', 'POST'])
@login_required
def submit_review():
    if request.method == 'GET':
        return render_template('review/review_confirmation.html',
                               game_id=-1,
                               review_h1="Review Error",
                               review_h2="Please submit a review through the game page.",
                               review_h3="Press OK to return to the browse menu.",
                               )

    username = session['username']
    user = utilities.getUser(username, repo.repo_instance)
    game_id = int(request.form['game_id'])
    rating = int(request.form['rating'])
    comment = request.form['comment']

    game = utilities.getGameById(repo.repo_instance, game_id)

    if game is not None:
        review = Review(user, game, rating, comment)

        try:
            # Add the review to the repository
            repo.repo_instance.add_review(review)

            return render_template('review/review_confirmation.html',
                                   game_id=game_id,
                                   review_h1="Review Confirmation",
                                   review_h2="Review submitted successfully!",
                                   review_h3="Thank you for your review!",
                                   )
        except RepositoryException as e:
            flash("An error occurred while submitting your review. Please try again.", "error")
            return redirect(url_for('browse.browse'))
    else:
        return render_template('review/review_confirmation.html',
                               game_id=-1,
                               review_h1="Review Error",
                               review_h2="Game Not Found. Please try again.",
                               review_h3="Press OK to return to the browse menu.",
                               )