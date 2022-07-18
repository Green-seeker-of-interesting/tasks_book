from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length
 

class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(),Email()])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=2, max=100)])
    remember = BooleanField("Запомнить", default = False)
    submit = SubmitField("Войти")


class RegistrForm(FlaskForm):
    name = StringField("Имя: ", validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField("Email: ", validators=[DataRequired(),Email()])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100)])
    psw_chek = PasswordField("Повторите пароль: ", validators=[DataRequired(), Length(min=4, max=100)])
    submit = SubmitField("Регистрация")


class CreateProjectFrom(FlaskForm):
     name = StringField("Название проекта", validators=[DataRequired(), Length(min=4, max=100)])
     submit = SubmitField("Создать")