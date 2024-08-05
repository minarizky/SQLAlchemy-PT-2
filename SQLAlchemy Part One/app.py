from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users/list.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url'] or None
        
        user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(user)
        db.session.commit()
        
        return redirect('/users')
    
    return render_template('users/new.html')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url'] or user.image_url
        
        db.session.commit()
        
        return redirect(f'/users/{user.id}')
    
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, redirect, render_template, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users/list.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url'] or None
        
        user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(user)
        db.session.commit()
        
        return redirect('/users')
    
    return render_template('users/new.html')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('users/detail.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        
        return redirect(f'/users/{user_id}')
    
    return render_template('posts/new.html', user=user)

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/detail.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        
        db.session.commit()
        
        return redirect(f'/posts/{post.id}')
    
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/users/{post.user_id}')

if __name__ == '__main__':
    app.run(debug=True)
