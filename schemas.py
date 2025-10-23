from app import db

from marshmallow import Schema, fields

from models import User, Post, Comment


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    type_category = fields.Str(required=True)
    is_active = fields.Bool()

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(required = True)
    is_active = fields.Bool(load_default=True)
    
class UserCredentialsSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    password = fields.Str(required=True)
    role = fields.Str(required=True)
    created_at = fields.DateTime(required = True)
    is_active = fields.Bool()


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(allow_none=True)
    content = fields.Str(allow_none=True)
    created_at = fields.DateTime(allow_none=True)
    update_at = fields.DateTime(allow_none=True)
    user_id = fields.Int()
    is_active = fields.Bool()
    category_id = fields.Int()
    category = fields.Nested(CategorySchema, only=["type_category"], dump_only=True)
    autor = fields.Nested(UserSchema, only=["id", "name", "email"], dump_only=True)


class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    text_comment = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    update_at = fields.DateTime(allow_none=True)
    is_active = fields.Bool()
    user_id = fields.Int()
    post_id = fields.Int()
    post = fields.Nested(PostSchema, only=["id", "title"], dump_only=True)
    autor = fields.Nested(UserSchema, only=["id", "name"], dump_only=True)
    
class RegisterSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    role = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

    
class LoginSchema(Schema):
    email = fields.Email(required= True)
    password = fields.Str(required=True, load_only= True)
