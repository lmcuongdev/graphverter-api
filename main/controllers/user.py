from main import app
from main.common.decorators import user_authenticated
from main.schemas.user import UserSchema


@app.route('/users/me', methods=['GET'])
@user_authenticated
def get_user_data(user, *__):
    return UserSchema().jsonify(user)
