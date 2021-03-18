from flask import Blueprint

blueprints = {
    "user": Blueprint(
                'user_blueprint',
                'app.routes.user_route',
                url_prefix='/user'
            ),
    "book": Blueprint(
                'book_blueprint',
                'app.routes.book_route',
                url_prefix='/book'
            ),
    "auth": Blueprint(
                'auth_blueprint',
                'app.routes.auth_route',
                url_prefix='/auth'
            )
}

from . import user_route, book_route, auth_route