import pytest

from flask import session


def test_register(client):
    # Check that we can retrieve the register page with a GET request.
    response_code = client.get('/auth/register').status_code
    assert response_code == 200

    # Check that we can retrieve the register page with a POST request.
    # Should result in a succesful registration and a redirect to the login page.
    response = client.post(
        '/auth/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == '/auth/login'


# Test each error case of registering a user.
@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required!'),
        ('er', '', b'Your username is too short!'),
        ('test', '', b'Your password is required!'),
        ('test', 'test', b'Password must be at least 8 characters long, contain an uppercase, lowercase, digit and special character'),
        ('fmercury', 'Test#6^0', b'Your username is already taken. Please try again.'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page with a GET request.
    status_code = client.get('/auth/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == '/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session, meaning a successful logout process.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'This is a game library website created for the 2023 S2 version of Computer Science 235' in response.data


def test_browse(client):
    # Check that we can retrieve the browse page.
    response = client.get('/browse/')
    assert response.status_code == 200
    assert b'Available Games' in response.data


def test_login_required_to_view_wishlist(client):
    # Check that we cannot retrieve the wishlist page as a guest user.
    # Should automatically redirect to the login page.
    response = client.get('/wishlist/')
    assert response.headers['Location'] == '/auth/login'

def test_wishlist(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the wishlist page.
    response = client.get('/wishlist/')
    assert response.status_code == 200
    assert b'Your wishlist is empty!' in response.data

def test_login_required_to_review(client):
    response = client.post('/review/submit_review')
    assert response.headers['Location'] == '/auth/login'


def test_review_left_successfully(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the game details page.
    response = client.get('/browse/details?id=7940')
    assert response.status_code == 200

    # POST a review.
    response = client.post(
        '/review/submit_review',
        data={
            'game_id': 7940,
            'rating': 5,
            'comment': 'This is a test comment'
        }
    )

    # Check that the comment now appears on the game details page.
    response = client.get('/browse/details?id=7940')
    assert response.status_code == 200
    assert b'This is a test comment' in response.data


def test_login_required_to_wishlist(client):
    response = client.post(
        '/wishlist/add_to_wishlist',
        data={
            'game_id': 7940
        }
    )
    assert response.headers['Location'] == '/auth/login'


def test_e2e_add_to_wishlist(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the game details page.
    response = client.get('/browse/details?id=7940')
    assert response.status_code == 200

    # POST a review.
    response = client.post(
        '/wishlist/add_to_wishlist',
        data={
            'game_id': 7940
        }
    )

    # Check that the comment now appears on the game details page.
    response = client.get('/wishlist/')
    assert response.status_code == 200
    assert b'Call of Duty' in response.data


def test_e2e_remove_from_wishlist(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the game details page.
    response = client.get('/browse/details?id=7940')
    assert response.status_code == 200

    # POST a review.
    response = client.post(
        '/wishlist/add_to_wishlist',
        data={
            'game_id': 7940
        }
    )

    # Check that the comment now appears on the game details page.
    response = client.get('/wishlist/')
    assert response.status_code == 200
    assert b'Call of Duty' in response.data

    # POST a review.
    response = client.post(
        '/wishlist/remove',
        data={
            'game_id': 7940
        }
    )

    # Check that the comment now appears on the game details page.
    response = client.get('/wishlist/')
    assert response.status_code == 200
    assert b'Call of Duty' not in response.data

