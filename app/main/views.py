from flask import render_template,request,url_for,redirect,flash,abort
from . import main
from flask_login import login_required, current_user
from ..models import *
from .forms import UpdateProfile
from .. import db,photos


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to my personal Blog'
    quotes = get_quotes()
    blogs = Blog.query.all()
    return render_template('index.html', title = title, quote = quotes,blogs=blogs)

@main.route('/blog/new', methods = ['GET','POST'])    
@login_required
def new_blog():
    subscribers = Subscriber.query.all()
    form = CreateBlogForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id =  current_user._get_current_object().id
        blog = Blog(title=title,content=content,user_id=user_id)
        blog.save()
       
        for subscriber in subscribers:
            mail_message("New Blog Post","email/new_blog",subscriber.email,blog=blog)
        return redirect(url_for('main.index'))
        flash('Anew blog has been posted by you')
    
    return render_template('newblog.html', form = form)
    





@main.route('/user/<uname>')
def profile(uname):
    form = UpdateProfile()

    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save()
        return redirect(url_for('.profile',name = name))    

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))
        
    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))    
    



    




        





