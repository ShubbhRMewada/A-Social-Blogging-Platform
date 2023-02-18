from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flaskblog import bcrypt

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)



# For User Interaction.

user_resource_fields = {
    'id':fields.Integer,
    'username':fields.String,
    'email':fields.String,
    'password':fields.String
}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # posts = db.relationship('Post', backref='author', lazy=True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("username", type=str, help="Username is required")
user_put_args.add_argument("email", type=str, help="Email is required")
user_put_args.add_argument("password", type=str, help="Password is required")
user_put_args.add_argument("image_file", type=str, help="Image is required")

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("username", type=str, help="Username is required",required=True)
user_post_args.add_argument("email", type=str, help="Email is required",required=True)
user_post_args.add_argument("password", type=str, help="Password is required",required=True)
user_post_args.add_argument("image_file", type=str, help="Image is required")

class User_API(Resource):

    @marshal_with(user_resource_fields)
    def get(self,id):
        user = User.query.filter_by(id=id).first()
        if user:
            return user
        return abort(409, message="User Doesn't exists")

    @marshal_with(user_resource_fields)
    def put(self,id):
        args = user_put_args.parse_args()
        user = User.query.filter_by(id=id).first()
        if user:
            if args['username']:
                user.username = args['username'] 
            if args['email']:
                    user.email = args['email'] 
            if args['password']:
                hashed_password = bcrypt.generate_password_hash(args['password']).decode('utf-8')
                user.password = hashed_password
            if args['image_file']:
                user.image_file = args['image_file'] 
            
            db.session.commit()
            return user
        
        return abort(409, message="User Doesn't exists")  
        
    @marshal_with(user_resource_fields)
    def post(self,id):
        args = user_post_args.parse_args()
        user = User.query.filter_by(id=id).first()
        if user:
            return abort(409, message="User Already exists")

        hashed_password = bcrypt.generate_password_hash(args['password']).decode('utf-8')
        user = User(username=args['username'],email=args['email'],password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @marshal_with(user_resource_fields)
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return user 

        return abort(409, message="User Doesn't exists")


# For getting all the users.
class All_User_API(Resource):

    @marshal_with(user_resource_fields)
    def get(self):
        user = User.query.all()
        return user



# For Post Interaction
        
post_resource_fields = {
    'id':fields.Integer,
    'title':fields.String,
    'date_posted':fields.String,
    'content':fields.String,
    # 'user_id':fields.String,
    'image_file':fields.String
}

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')


  
post_put_args = reqparse.RequestParser()
post_put_args.add_argument("title", type=str, help="Title is required")
post_put_args.add_argument("content", type=str, help="Content is required")
# post_put_args.add_argument("user_id", type=int, help="UserID is required")
post_put_args.add_argument("image_file", type=str, help="Image is required")

post_post_args = reqparse.RequestParser()
post_post_args.add_argument("title", type=str, help="Title is required",required=True)
post_post_args.add_argument("content", type=str, help="Content is required",required=True)
# post_post_args.add_argument("user_id", type=int, help="UserID is required")
post_post_args.add_argument("image_file", type=str, help="Image is required")

class Post_API(Resource):

    @marshal_with(post_resource_fields)
    def get(self,id):
        post = Post.query.filter_by(id=id).first()
        if post:
            return post
        return abort(409, message="Post Doesn't exists")

    @marshal_with(post_resource_fields)
    def put(self,id):
        args = post_put_args.parse_args()
        post = Post.query.filter_by(id=id).first()
        if post:
            if args['title']:
                post.title = args['title'] 
            if args['content']:
                post.content = args['content'] 
            # if args['user_id']:
            #     post.user_id = args['user_id'] 
            if args['image_file']:
                post.image_file = args['image_file'] 
            
            db.session.commit()
            return post
        
        return abort(409, message="Post Doesn't exists")  
        
    @marshal_with(post_resource_fields)
    def post(self,id):
        args = post_post_args.parse_args()
        post = Post.query.filter_by(id=id).first()
        if post:
            return abort(409, message="Post Already exists")
        # post = Post(title=args['title'],content=args['content'],user_id=args['user_id'],image_file=args['image_file'])
        post = Post(title=args['title'],content=args['content'],image_file=args['image_file'])
        db.session.add(post)
        db.session.commit()
        return post
    
    @marshal_with(post_resource_fields)
    def delete(self, id):
        post = Post.query.filter_by(id=id).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return post 

        return abort(409, message="Post Doesn't exists")


class All_Post_API(Resource):

    @marshal_with(post_resource_fields)
    def get(self):
        post = Post.query.all()
        return post





api.add_resource(User_API,'/user/<int:id>')
api.add_resource(All_User_API,'/user')
api.add_resource(Post_API,'/posts/<int:id>')
api.add_resource(All_Post_API,'/posts')
db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
