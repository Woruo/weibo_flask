from routes import *
from utils import log
from models.weibo import Weibo, WCollect, WFavorite, Comment, CFavorite
from models.user import User, Follow

main = Blueprint('userApi', __name__)

@main.route('/follow', methods=['POST'])
@login_required
def follow(user):
    form = request.form
    u_id = form.get('u_id', None)
    status, data, msg = user.follow_person(u_id)
    return api_response(status, data, msg)
