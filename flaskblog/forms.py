from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Post
from flask_login import current_user



class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(),Email()])                 
    password = PasswordField('Password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    # These are just function parameter variables and can be named however you see fit 
    # since you're passing the username (or email) form field directly into the function through the function declaration. 
    # i.e. validate_<field_name>
    # Your validation methods have to follow the validate_<field_name> convention specified within flask-wtf 
    # In your example, your form fields are: [username, email, password, confirm_password, submit] 
    # so your validation methods would have to be: validate_username(...), validate_email(...), validate_password(...), etc... 
    # If you want to have a different validation method name you would also have to correspondingly rename your form fields appropriately.

    def validate_username(self, username):
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),Email()])                 
    password = PasswordField('Password',
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('LogIn')


class UpdatePassword(FlaskForm):
    update_password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[EqualTo('update_password')])
    submit = SubmitField('Update')                                    
    
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(),Email()])                 
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    
    submit = SubmitField('Update')


    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username= username.data).first()
            if user:
                raise ValidationError('This username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email= email.data).first()
            if user:
                raise ValidationError('This email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Share an Image', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Post')


class Search(FlaskForm):
    key = StringField('Enter the Username', validators=[DataRequired()])
    submit = SubmitField('Search')


class DeleteForm(FlaskForm):
    value = BooleanField('Do you really want to delete your account? All your data will be lost!')
    submit = SubmitField('Submit',validators=[DataRequired()])

class CommentForm(FlaskForm):
    value = TextAreaField('Add a new Comment')
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')