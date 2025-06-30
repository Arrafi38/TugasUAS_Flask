from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)
api = Api(app)

# Database Model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"

# API Resources
user_post_args = reqparse.RequestParser()
user_post_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_post_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

user_update_args = reqparse.RequestParser()
user_update_args.add_argument('name', type=str, help="Name of the user")
user_update_args.add_argument('email', type=str, help="Email of the user")

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(user_fields)
    def post(self):
        args = user_post_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

class User(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message=f"User with id {user_id} not found")
        return user
    
    @marshal_with(user_fields)
    def put(self, user_id):
        args = user_update_args.parse_args()
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message=f"User with id {user_id} not found")
        
        if args['name']:
            user.name = args['name']
        if args['email']:
            user.email = args['email']
            
        db.session.commit()
        return user
    
    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message=f"User with id {user_id} not found")
        
        db.session.delete(user)
        db.session.commit()
        return {'message': f"User with id {user_id} deleted successfully"}, 200

api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:user_id>')

# Web Routes
@app.route('/')
def index():
    users = UserModel.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        if not name or not email:
            flash('Name and email are required!')
            return redirect(url_for('add_user'))
        
        try:
            new_user = UserModel(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('User added successfully!')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            flash('Error adding user. Name or email may already exist.')
            return redirect(url_for('add_user'))
    
    return render_template('add_user.html')

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = UserModel.query.get_or_404(user_id)
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        if not name or not email:
            flash('Name and email are required!')
            return redirect(url_for('edit_user', user_id=user_id))
        
        try:
            user.name = name
            user.email = email
            db.session.commit()
            flash('User updated successfully!')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            flash('Error updating user. Name or email may already exist.')
            return redirect(url_for('edit_user', user_id=user_id))
    
    return render_template('edit_user.html', user=user)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = UserModel.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!')
    except:
        db.session.rollback()
        flash('Error deleting user.')
    
    return redirect(url_for('index'))

# Templates folder
@app.route('/create_templates')
def create_templates():
    return "Templates created! Check your project directory."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)