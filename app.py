from flask import Flask, request
from flask_jwt_extended import JWTManager
from models import(
    db,
    User,
    Post,
    Comment
)

#Lo use para que me pueda funcionar el frond
from flask_cors import CORS

from schemas import CategorySchema, UserSchema, UserCredentialsSchema, PostSchema, CommentSchema, RegisterSchema, LoginSchema

from views import *

app = Flask(__name__)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']=(
    'mysql+pymysql://root:@localhost/efi-segundo-semestre'
)
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'cualquier-cosa'

jwt = JWTManager(app)
db.init_app(app)

#Autenticacion
app.add_url_rule(
    '/register',
    view_func=UserRegisterAPI.as_view('user_register_api'),
    methods=['POST']
)

app.add_url_rule(
    '/login',
    view_func=UserLoginAPI.as_view('user_login_api'),
    methods=['POST']
)

#Post
app.add_url_rule(
    '/post',
    view_func=ListPostsAPI.as_view('list_posts_api'),
    methods=['GET']
)

app.add_url_rule(
    '/post/<id>',
    view_func=ListOnePostAPI.as_view('list_one_post_api'),
    methods=['GET']
)


app.add_url_rule(
    '/post',
    view_func=NewPostsAPI.as_view('new_post_api'),
    methods=['POST']
)

app.add_url_rule(
    '/post/<id>',
    view_func=DeletePostAPI.as_view('delete_post_api'),
    methods=['PATCH']
)

app.add_url_rule(
    '/post/<id>',
    view_func=EditPostAPI.as_view('edit_post_api'),
    methods=['PUT']
)

#Comentarios
app.add_url_rule(
    '/post/<id>/comments',
    view_func=ListCommentsOnePostAPI.as_view('comments_post_api'),
    methods=['GET']
)

app.add_url_rule(
    '/post/<id>/comment',
    view_func=NewCommentOnePostAPI.as_view('new_comment_one_post_api'),
    methods=['POST']
)

app.add_url_rule(
    '/post/comment/<id>',
    view_func=DeletePostCommentAPI.as_view('delete_post_comment_api'),
    methods=['PATCH']
)

#Categorias
app.add_url_rule(
    '/categories',
    view_func=CetegoryAPI.as_view('new_category_api'),
    methods=['GET','POST']
)

app.add_url_rule(
    '/categories/<id>',
    view_func=EditDeleteCategoryAPI.as_view('edit_category_api'),
    methods=['PUT','PATCH']
)

#Usuarios
app.add_url_rule(
    '/users',
    view_func=UsersAPI.as_view('users_api'),
    methods=['GET']
)

app.add_url_rule(
    '/users/<id>',
    view_func=MyUserApi.as_view('my_users_api'),
    methods=['GET']
)
app.add_url_rule(
    '/users/<id>/role',
    view_func=EditUserAPI.as_view('edit_user_api'),
    methods=['PATCH']
)

app.add_url_rule(
    '/users/<id>',
    view_func=DeleteUserAPI.as_view('delete_user_api'),
    methods = ['PATCH']
)

#Estadisticas
app.add_url_rule(
    '/stats',
    view_func=StatsAPI.as_view('stats_api'),
    methods=['GET']
)
if __name__ == '__main__':
    app.run(debug=True)