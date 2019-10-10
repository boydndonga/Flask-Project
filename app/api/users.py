from app.api import bp
from flask import jsonify
from app.models import User
from flask import url_for, request
from app.api.errors import bad_request
from app import db



# API endpoint to get user with an id
@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


# API endpoint to create user
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    if 'username' not in data or'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password')

    if User.query.filter_by(username=data['username']).first():
        return bad_request('Please use a different username')

    if User.query.filter_by(email=data['email']).first():
        return bad_request('Please use a different email address')

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

# API endpoint to update user
@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)

    if 'username' in data and data['username'] != user.username and  \
            User.query.filter_by(username=data['username']).first():
        return bad_request('Please use a different username')

    if 'email' in data and data['username'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('Please use a different email address')

    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

