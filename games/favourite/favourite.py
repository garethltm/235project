from flask import Blueprint, render_template, request, redirect, url_for, flash
from games.domainmodel.model import User, Wishlist
from games.browse.services import getGameById
import games.wishlist.services as wishlist_services
from games.utilities import utilities
import games.adapters.repository as repo
from flask import jsonify