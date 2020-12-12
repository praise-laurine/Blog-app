from flask import render_template,request,url_for,redirect,flash,abort
from . import main
from ..models import *
from .. import db


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to my personal Blog'
    quotes = get_quotes()
    blogs = Blog.query.all()
    return render_template('index.html', title = title, quote = quotes,blogs=blogs)



