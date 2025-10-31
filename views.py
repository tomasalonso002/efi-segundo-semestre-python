from datetime import datetime, timedelta
from functools import wraps

from flask import request, jsonify
from marshmallow import ValidationError
from flask.views import MethodView

from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt
)

from passlib.hash import bcrypt

from app import db
from models import User, UserCredentials, Post, Comment, Category
from schemas import CategorySchema, UserSchema, UserCredentialsSchema, PostSchema, CommentSchema, RegisterSchema, LoginSchema


#role_requiered
def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get('role')
            if not role or role not in allowed_roles:
                return {"Error":"Rol no autorizado"}
            return fn(*args, **kwargs)
        return wrapper
    return decorator

#Autenticación
#Register
class UserRegisterAPI(MethodView):
    def post(self):
        try:
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            return jsonify({
                "Error": "error de validacion",
                "detalles": err.messages
                }),400
        if User.query.filter((User.email==data["email"]) | (User.name == data["name"])).first():
            return jsonify({
                "Error":"Email o nombre en uso"
                }),400
        
        new_user = User(
            name = data["name"],
            email=data["email"],
            is_active=True,
            created_at = datetime.now()
            )
        db.session.add(new_user)
        db.session.flush() # sincroniza la db sin hace el commit (asigna a user un id)
        
        password_hash = bcrypt.hash(data["password"])

        credenciales = UserCredentials(
            user_id = new_user.id,
            password_hash = password_hash,
            role = data["role"],
            is_active=True,
            created_at = datetime.now()
        )
        
        db.session.add(credenciales)
        db.session.commit()
        return jsonify({
            "menssage":"Usuario creado correctamente",
            "id": new_user.id
        }),201
#Login
class UserLoginAPI(MethodView):
    def post(self):
        try:
            data = LoginSchema().load(request.json)
        except ValidationError as err:
            return {"Error":err.messages},400
        
        user = User.query.filter_by(email=data["email"]).first()
        
        if not user or not user.credentials:
            return {"Error":{"credentials":["Invalidas"]}},401
        
        if not bcrypt.verify(data["password"], user.credentials.password_hash):
            return {"Error":{"credentials":["Invalidas"]}},401
        
        identity = str(user.id)
        additional_claims = {
            "id":user.id,
            "email":user.email,
            "name": user.name,
            "role":user.credentials.role
        }
        token = create_access_token(
            identity=identity,
            additional_claims=additional_claims,
            expires_delta = timedelta(hours=24)
        )
        return jsonify({
            "access_token":token
        }),200


#Post
#GET
class ListPostsAPI(MethodView):
    def get(self):
        posts = Post.query.all()
        if posts:
            return UserSchema(many=True).dump(posts),200
        else:
            return jsonify({"Error": "No hay post"}),404

class ListOnePostAPI(MethodView):
    def get(self, id):
        post = Post.query.get(id)
        if post:
            return UserSchema().dump(post),200
        else:
            return jsonify({"Error": "No se encontro ese post"}),404

#POST
class NewPostsAPI(MethodView):
    @jwt_required()
    @role_required('user')
    def post(self):
        try:
            data = PostSchema().load(request.json)
        except ValidationError as err:
            return{"Error":err.messages},400
        new_post = Post(
            title = data["title"],
            content = data["content"],
            created_at = datetime.now(),
            user_id = data["user_id"],
            is_active = True,
            category_id = data["category_id"]
        )
        db.session.add(new_post)
        db.session.commit()
        return{
            "message":"Post creado correctamente"
        },200


#DELETE/PUTCH
class DeletePostAPI(MethodView):
    @jwt_required()
    @role_required('user','moderador','admin')
    def patch(self,id):
        posteo = Post.query.get(id)
        if not posteo:
            print('no encontrado')
            return jsonify({"message":"No se encontro el post"})
        if posteo.is_active == False:
            print('es falso')
            return jsonify({"message":"No se encontro el post"})
        
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        user_role = user.credentials.role
        print(user_role)
        
        if  user_role in ['admin','moderador']:
            posteo.is_active = False
            db.session.commit()
            print("soy admin o mod")
            return jsonify({"message":"Post borrado"}),200
        if int(posteo.user_id) != int(current_user_id):
            return jsonify({"Error":"No estas autorizado a borrar este post"}),403
        posteo.is_active = False
        db.session.commit()
        return jsonify({"message":"Post borrado"}),200

class EditPostAPI(MethodView):
   @jwt_required()
   @role_required('user','moderador', 'admin')
   def put(self,id):
        posteo = Post.query.get(id)
        if not posteo:
            return jsonify({"message": "El post no existe"})
        if posteo.is_active == False:
             return jsonify({"message": "El post no existe(false)"})

        try:
            data = PostSchema().load(request.json)        
        except ValidationError as err:
            return {"Error": err.messages}, 404
        
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        user_role = user.credentials.role
        
        if  user_role in ['admin','moderador']:
            posteo.title = data["title"]
            posteo.content = data["content"]
            posteo.created_at = posteo.created_at
            posteo.update_at = datetime.now()
            posteo.user_id = data["user_id"] 
            posteo.is_active = True
            posteo.category_id = data["category_id"] 
            db.session.commit()
            return jsonify({"message":"Posteo Editado correctamente"}),200
        
        if int(posteo.user_id) != int(current_user_id):
            return jsonify({"Error":"No estas autorizado a editar este posteo"}),403
        
        posteo.title = data["title"]
        posteo.content = data["content"]
        posteo.created_at = posteo.created_at
        posteo.update_at = datetime.now()
        posteo.user_id = data["user_id"] 
        posteo.is_active = True
        posteo.category_id = data["category_id"]     
        db.session.commit()
        return jsonify({"message":"Posteo Editado correctamente"}),200
    
#Comentarios
#GET
class ListCommentsOnePostAPI(MethodView):
    def get(self, id):
        comentarios = Comment.query.filter_by(post_id=id).all()
        if comentarios:
            return CommentSchema(many=True).dump(comentarios),200
        else:
            return jsonify({"Error":"No hay comentarios en este post"}),404

#POST
class NewCommentOnePostAPI(MethodView):
    @jwt_required()
    @role_required('user','admin','moderador')
    
    def post(self,id):
        try:
            data = CommentSchema().load(request.json)
        except ValidationError as err:
            return {"Error": err.messages}, 404
        newComment = Comment(
            text_comment = data["text_comment"],
            created_at = datetime.now(),
            is_active = True,
            user_id = data["user_id"],
            post_id = id
        )
        db.session.add(newComment)
        db.session.commit()
        return jsonify({
            "message":"Comentario creado correctamente"
        })

#DELETE/PUTCH
class DeletePostCommentAPI(MethodView):
    @jwt_required()
    @role_required('user','moderador','admin')
    def patch(self, id):
        comentario = Comment.query.get(id)
        if not comentario:
            return jsonify({"message": "Comentario no encontrado"}),404
        if comentario.is_active == False:
            return jsonify({"message": "Comentario no encontrado"}),404
        #extract the user_role and user_id of token
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        user_role = user.credentials.role
        #si el rol es admin o moderador, lo borra, sino verifica el autor del comment, si no es el autor, return sino borra 
        if  user_role in ['admin','moderador']:
            comentario.is_active = False
            db.session.commit()
            return jsonify({"message":"Comentario borrado"}),200
        if int(comentario.user_id) != int(current_user_id):
            return jsonify({"Error":"No estas autorizado a borrar este comentario"}),403
        comentario.is_active = False
        db.session.commit()
        return jsonify({"message":"Comentario borrado"}),200

#Categorias
#GET and POST
class CetegoryAPI(MethodView):
    def get(self):
        categories = Category.query.all()
        if categories:
            return CategorySchema(many=True).dump(categories),200
        else:
            return jsonify({"Error":"No hay caregorias"})    
    
    @jwt_required()
    @role_required('moderador','admin')
    def post(self):
        try:
            date = CategorySchema().load(request.json)
        except ValidationError as err:
            return {"Error":err.messages},400
        
        newCategory = Category (
            type_category = date["type_category"],
            is_active = True
        )
        db.session.add(newCategory)
        db.session.commit()
        return jsonify({"message":"Categoria creada con exito"}),201
#PUT and DELETE/PATCH

class EditDeleteCategoryAPI(MethodView):
    @jwt_required()
    @role_required('moderador','admin')
    def put(self, id):
        categoria = Category.query.get(id)
        if not categoria:
            return jsonify({"message":"No se encontro la categoria"}),404
        if categoria.is_active == False:
            return jsonify({"message":"No se encontro la categoria(false)"}),404

        try:
            data = CategorySchema().load(request.json)
        except ValidationError as err:
            return {"Error": err.messages},404
        
        categoria.type_category = data["type_category"]
        db.session.commit()
        return jsonify({"message": "Categoria modificada con exito"})

    
    @jwt_required()
    @role_required("admin")
    def patch(self,id):
        categoria = Category.query.get(id)

        if not categoria:
            return jsonify({"message":"No existe esa categoria"}),404
        if categoria.is_active == False:
            return jsonify({"message":"No existe esa categoria(false)"}),404

        categoria.is_active = False
        db.session.commit()
        return jsonify({"message": "Categoria eliminada con exito"})

        
#Usuarios
#GET
class UsersAPI(MethodView):
    @jwt_required()
    @role_required('admin')
    def get(self):
        usuarios = User.query.filter_by(is_active=1)
        if not usuarios:
            return jsonify({"message":"No se encontraron usuarios"}),404
        return UserSchema(many=True).dump(usuarios)
    
class MyUserApi(MethodView):
    @jwt_required()
    @role_required('user','admin')
    def get(self,id):
        usuario = User.query.get(id)

        if not usuario:
            return jsonify({'message':'Usuario no encntrado'}),404
        if usuario.is_active == False:
            return jsonify({'message':'Usuario no encontrado'}),404
        
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        user_id = user.id
        user_role = user.credentials.role
        
        if user_role == 'admin':
            return {
                'id':user.id,
                'name': user.name,
                'email': user.email
                    },200
        if int(user_id) == int(id):
            return {
                'id':user.id,
                'name': user.name,
                'email': user.email
                    },200
        
        return jsonify({'No estas autorizado a consultar un perfil no propio'}),404

#PATCH
class EditUserAPI(MethodView):
    @jwt_required()
    @role_required('admin')
    def patch(self,id):
        usuario = UserCredentials.query.filter_by(user_id = id).first()

        if not usuario:
            return jsonify({'message':'Usuario no encontrado'}),404
        if usuario.is_active == False:
            return jsonify({'message':'Usuario no encontrado'}),404

        try:
            data = UserCredentialsSchema(partial=True).load(request.json)
        except ValidationError as err:
            return {'Error': err.messages},404
        
        usuario.role = data['role']
        db.session.commit()
        return jsonify({"message":"Usuario editado correctamente"}),200

#DELETE/PATCH
class DeleteUserAPI(MethodView):
    @jwt_required()
    @role_required('admin')
    def patch(self, id):
        usuario = User.query.get(id)
        if not usuario:
            return jsonify({"Error":"Este usuario no existe"}),404
        if usuario.is_active == False:
            return jsonify({"Error":"Este usuario no existe"}),404
        
        credencial_usuario = UserCredentials.query.filter_by(user_id = id).first()
        
        credencial_usuario.is_active = False
        usuario.is_active = False
        db.session.commit()
        return jsonify({"message":"Usuario borrado correctamente"}),200
    

#Estadisticas
#GET
class StatsAPI(MethodView):
    @jwt_required()
    @role_required('admin', 'moderador')
    def get(self):
        posteos = Post.query.filter_by(is_active=1).count()
        comentarios = Comment.query.filter_by(is_active=1).count()
        usuarios = User.query.filter_by(is_active=1).count()
        
        una_semana_atras = datetime.now() - timedelta( days = 7)
        post_lask_week = Post.query.filter(Post.created_at >= una_semana_atras).count()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        user_role = user.credentials.role
        if user_role == "admin":
            return jsonify({
                "Total_post":posteos,
                "Total_comments":comentarios,
                "Total_users":usuarios,
                "post_lask_week": post_lask_week
            })
        else:
            return jsonify({
                "Total_post":posteos,
                "Total_comments":comentarios,
                "Total_users":usuarios
            })