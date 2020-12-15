from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class BlogForm(FlaskForm):

    title = StringField('Blog title',validators=[Required()])
    text = TextAreaField('Text',validators=[Required()])
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
    text = TextAreaField('Leave a comment:',validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit') 
