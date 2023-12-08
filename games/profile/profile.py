from games.authentication.authentication import login_required
from games.utilities.utilities import paginateLists, getUser
from flask import Blueprint, render_template, session, request
import games.adapters.repository as repo

profile = Blueprint('profile', __name__, url_prefix='/profile', static_folder='static', template_folder='templates')


@profile.route('/')
@login_required
def profile_detail():
    username = session['username']
    user = repo.repo_instance.getUser(username)
    reviews = repo.repo_instance.getAllReviews()
    user_reviews = [review for review in reviews if review.user == user]
    user_reviews = user_reviews[::-1]
    wishlist = repo.repo_instance.get_wishlist(user)

    per_page = 10
    total_page = (len(user_reviews) // per_page) + 1 if len(user_reviews) % per_page != 0 else len(
        user_reviews) // per_page
    page = min(max(request.args.get('page', 1, type=int), 1), total_page)

    paginated_reviews = paginateLists(user_reviews, page, per_page)

    attributes = []
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


    return render_template('profile/profile.html',
                           page=page,
                           total_page=total_page,
                           first_page=first_page,
                           last_page=last_page,
                           next_page=next_page,
                           prev_page=prev_page,
                           user_reviews=paginated_reviews,
                           wishlist=wishlist,
                           user=user)
