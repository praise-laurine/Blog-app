from flask import render_template,request,url_for,redirect,flash,abort
from . import main
from .forms import BlogForm, CommentForm, UpdateProfile
from ..models import User, Comment , Blog
from flask_login import login_required, current_user
from .. import db, photos
import datetime
from ..request import getQuotes

@main.route('/')
def index():
    
    '''
    View root page function that returns the index page and its data
    '''

    blogs = Blog.query.all()
    title = 'Home - Welcome to Blogs Online  Website'
    quote = getQuotes()
    quote1 = getQuotes()
    quote2 = getQuotes()
    quote3 = getQuotes()



    return render_template('index.html', title = title, blogs=blogs, quote=quote ,quote1=quote1,quote2=quote2,quote3=quote3 )

@main.route('/blog/new', methods = ['GET','POST'])
@login_required
def new_blog():
    blog_form = BlogForm()
    if blog_form.validate_on_submit():
        title = blog_form.title.data
        blog = blog_form.text.data

        # Updated blog instance
        new_blog = Blog(blog_title=title,blog_content=blog,username=current_user.username,likes=0,dislikes=0)

        # Save blog method
        new_blog.save_blog()
        return redirect(url_for('.index'))

    title = 'New blog'
    return render_template('new_blog.html',title = title,blog_form=blog_form )  

@main.route('/blog/<int:id>', methods = ['GET','POST'])
def blog(id):
    blog = Blog.get_blog(id)
    posted_date = blog.posted.strftime('%b %d, %Y')

    if request.args.get("like"):
        blog.likes = blog.likes + 1

        db.session.add(blog)
        db.session.commit()

        return redirect("/blog/{blog_id}".format(blog_id=blog.id))

    elif request.args.get("dislike"):
        blog.dislikes = blog.dislikes + 1

        db.session.add(blog)
        db.session.commit()

        return redirect("/blog/{blog_id}".format(blog_id=blog.id))
    
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,blog_id = blog)

        new_comment.save_comment()


    comments = Comment.get_comments(blog)
    
    
    return render_template("blog.html", blog = blog, date = posted_date, comment_form = comment_form, comments = comments)  

@main.route('/user/<uname>/blogs')
def user_blogs(uname):
    user = User.query.filter_by(username=uname).first()
    blogs = Blog.query.filter_by(user_id = user.id).all()
    blogs_count = Blog.count_blogs(uname)
    user_joined = user.date_joined.strftime('%b,%d,%y')
    
    return render_template("profile/blogs.html",user = user, blogs = blogs, blogs_count= blogs_count,date= user_joined)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

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

@main.route("/blog/<int:id>/update",methods = ['GET','POST'])
@login_required
def update_blog(id):
    blog = Blog.query.get_or_404(id)
    if blog.username != current_user.username:
        abort(403)
    blog_form = BlogForm()
    if blog_form.validate_on_submit():
        blog.blog_title = blog_form.title.data
        blog.blog_content = blog_form.text.data
        db.session.commit()
        flash('Your blog has been updated!', 'success')
        return redirect(url_for('main.blog', id=blog.id))
    elif request.method == 'GET':
        blog_form.title.data = blog.blog_title
        blog_form.text.data = blog.blog_content
    
    return render_template('new_blog.html',title = 'Update Blog',blog_form=blog_form )

@main.route("/blog/<int:id>/delete", methods=['POST'])
@login_required
def delete_blog(id):
    blog = Blog.query.get(id)
    if blog.username != current_user.username:
        abort(403)

    db.session.delete(blog)
    db.session.commit()

    flash('Your post has been deleted!', 'success')

    return redirect(url_for('main.index'))

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
