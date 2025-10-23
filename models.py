from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column (db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False)
    credentials = db.relationship(
        'UserCredentials', 
        back_populates='user', 
        uselist=False,
        cascade='all, delete-orphan'
    )
    def __str__(self):
        return self.name
    

class UserCredentials(db.Model):
    id = db.Column (db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    password_hash = db.Column(db.String(256), nullable = False, unique = False)
    created_at = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.String(100), default="user", nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    user = db.relationship('User', back_populates='credentials')
    
class Post(db.Model):
    id = db.Column (db.Integer, primary_key = True)
    title = db.Column(db.String(150), nullable = False)
    content = db.Column(db.Text, nullable= False)
    created_at = db.Column(db.DateTime, nullable = False)
    update_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable =False)
    category = db.relationship(
        "Category",
        backref = db.backref("posts", lazy=True)
    )
    autor = db.relationship(
        "User",
        backref = db.backref("posts", lazy=True)
    )
    def __str__(self):
        return self.title
    
class Comment(db.Model):
    id = db.Column (db.Integer, primary_key = True)
    text_comment = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False)
    update_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable= False)
    is_active = db.Column(db.Boolean, default=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable= False)
    
    post = db.relationship(
        "Post",
        backref = db.backref("comments", lazy=True)
    )
    autor = db.relationship(
        "User",
        backref = db.backref("comments", lazy=True)
    )
    
    def __str__(self):
        return self.text_comment
    
class Category(db.Model):
    id = db.Column (db.Integer, primary_key = True)
    type_category = db.Column(db.Text, nullable = False)
    is_active = db.Column(db.Boolean, default=True)
    
    def __str__(self):
        return self.type_category