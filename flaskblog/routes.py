import secrets, os
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, Search, UpdatePassword, DeleteForm, CommentForm, RequestResetForm, ResetPasswordForm
from flask import render_template,redirect, url_for,flash, request
from flaskblog.models import User,Post, Master_Servent, Like, Comment
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
@login_required
def home():
    masters = Master_Servent.query.filter_by(servent= current_user.id).all()
    user_id = [i.master for i in masters]
    user_id.append(current_user.id)
    user_id = set(user_id)
    posts=[]
    for i in user_id:
        posts.extend(Post.query.filter_by(user_id=i).all())
    
    return render_template('home.html',title="Home",db=db,Comment=Comment,Like=Like,posts=posts[-1::-1])



@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data, email=form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in!", 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Sign Up',form=form)



@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('account')) if next_page else redirect(url_for('home'))
        else:
            flash(f"Login Unsuccessful. Please check your email and password.", 'danger')
    return render_template('login.html',title='Login',form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn



@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static',filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html',title='Update', image_file=image_file, form= form)



def post_images(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_images', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = post_images(form.picture.data)
            post = Post(title=form.title.data, content= form.content.data, author = current_user, image_file=picture_file)
        else:
            post = Post(title=form.title.data, content= form.content.data, author = current_user)
        
        
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('home'))
    
    return render_template('create_post.html',title='Create',form=form, legend='New Post')


@app.route('/post/<int:post_id>',methods=['GET','POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        post = Comment(post_id=post_id,user_id=current_user.id,comments=form.value.data)
        form.value.data=""
        db.session.add(post)
        db.session.commit()
        # return render_template('post.html',post = Post.query.filter_by(id=post_id).first(),User=User,Like=Like,Comment=Comment, form=form)
        return redirect(url_for('post',post_id=post_id))
    
    return render_template('post.html',post = Post.query.filter_by(id=post_id).first(),User=User,Like=Like,Comment=Comment, form=form)


@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # if post.author != current_user:
    #         abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        
        if form.picture.data :
            post.image_file = post_images(form.picture.data)
        
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('home'))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html',title='Update Post', form = form, legend='Update Post')




@app.route('/post/<int:post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    post = Like.query.filter_by(post_id=post_id).all()
    for i in post:
        db.session.delete(i)
    comment = Comment.query.filter_by(post_id=post_id).all()
    for i in comment:
        db.session.delete(i)

    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('home'))
    


@app.route('/post/<int:user_id>/follow')
@login_required
def follow(user_id):
    servent = current_user.id
    user = User.query.get_or_404(user_id)
    master = user.id
    conn = Master_Servent(master=master,servent=servent)
    db.session.add(conn)
    db.session.commit()
    return redirect(url_for('profile',user_id=user_id))


@app.route('/post/<int:user_id>/unfollow')
@login_required
def unfollow(user_id):
    servent = current_user.id
    user = User.query.get_or_404(user_id)
    master = user.id
    conn = Master_Servent.query.filter_by(master=master , servent=servent)
    # When we use the filter method, we get a list in return. And the first element of the list is always the answer.
    db.session.delete(conn[0])
    db.session.commit()
    return redirect(url_for('profile',user_id=user_id))



@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    is_follower = True if Master_Servent.query.filter_by(master=user_id,servent=current_user.id).all() else False
    followers = Master_Servent.query.filter_by(master=user_id).all()
    followers = len(set(i.servent for i in followers))
    following = Master_Servent.query.filter_by(servent=user_id).all()
    following = len(set(i.master for i in following))
    
    return render_template('profile.html', title="Profile", user=user, post=user.posts[::-1],Comment=Comment,Like=Like, followers=followers,following=following, is_follower=is_follower)



@app.route('/search', methods=['GET','POST'])
@login_required
def search():
    form = Search()
    if form.validate_on_submit():
        available_users = list(User.query.filter(User.username.like('%' + form.key.data + '%')))
        masters_from_available_users =Master_Servent.query.filter_by(servent=current_user.id).all()
        return render_template('search.html',form=form,available_users=available_users, masters=[i.master for i in masters_from_available_users],Master_Servent=Master_Servent) if available_users else render_template('search.html',form=form,available_users=None,Master_Servent=Master_Servent)
    
    return render_template('search.html',title="Search",form=form,available_users='search',Master_Servent=Master_Servent)
    

@app.route('/followers/<int:user_id>')
@login_required
def followers(user_id):
    masters = Master_Servent.query.filter_by(servent=current_user.id).all()
    masters = set(i.master for i in masters)
    servents = Master_Servent.query.filter_by(master=current_user.id).all()
    servents = set(i.servent for i in servents)
    servents = [User.query.get(i) for i in servents]
    return render_template('followers.html',servents=servents,masters=masters)


@app.route('/following/<int:user_id>')
@login_required
def following(user_id):
    masters = Master_Servent.query.filter_by(servent=user_id).all()
    masters = set(i.master for i in masters)
    masters = [User.query.get(i) for i in masters]
    return render_template('following.html',masters=masters)


@app.route('/update_password/<int:user_id>',methods=['POST','GET'])
@login_required
def update_password(user_id):
    form = UpdatePassword()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.update_password.data).decode('utf-8')            
        current_user.password = hashed_password
        db.session.commit()
        flash('Your Password has been updated!','success')
        return redirect(url_for('account'))
    
    return render_template('update_password.html',form=form)


# In any case if the below given functions generates an error, use "db.session.rollback()" using the terminal.
# Error mostly occurs because the database is not commited properly i.e. "db.session.commit()" is pending.
@app.route('/delete_account',methods=['POST','GET'])
@login_required
def delete_account():
    form = DeleteForm()
    if form.validate_on_submit():
        if form.value.data:
            post = Post.query.filter_by(user_id = current_user.id).all()
            if post:
                for i in post:
                    db.session.delete(i)
            
            masters = Master_Servent.query.filter_by(master=current_user.id).all()
            servents = Master_Servent.query.filter_by(servent=current_user.id).all()

            for i in masters:
                db.session.delete(i)
            for i in servents:
                db.session.delete(i)
            
            user = User.query.get_or_404(current_user.id)
            if user:
                db.session.delete(user)
            
            posts = Like.query.filter_by(user_id=current_user.id).all()
            for i in posts:
                db.session.delete(i)
            
            posts = Comment.query.filter_by(user_id=current_user.id).all()
            for i in posts:
                db.session.delete(i)
            

            db.session.commit()

            flash('Your Account has been deleted!','success')
            return redirect(url_for('login'))

    return render_template('delete.html',form=form)

@app.route('/like/<int:post_id>',methods=['GET','POST'])
def like(post_id):
    querry = Like.query.filter_by(post_id=post_id,user_id=current_user.id).first()
    if not querry:
        post = Like(post_id=post_id,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post',post_id=post_id))
    else:
        db.session.delete(querry)
        db.session.commit()
        return redirect(url_for('post',post_id=post_id))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='dummy.mail.for.iitmproject@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)



@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)