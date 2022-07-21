from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length
 
from logic import prodject_worker as pjw

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
    name = StringField("Название проекта", validators=[DataRequired(), Length(max=250)])
    is_open = BooleanField("Открытый ? ", default = False)
    category = SelectField('Категория', choices=pjw.get_сategori_list_worker_tuple(), coerce=int)
    submit = SubmitField("Создать")


class CreateTaskForm(FlaskForm):
    title = StringField("Задчача ", validators=[DataRequired(), Length(max=250)])
    content = TextAreaField("Описание", validators=[DataRequired()])
    deadline = DateField("Срок задачи")
    priority = SelectField('Категория', choices=pjw.get_priority_list_worker_tuple(), coerce=int)
    submit = SubmitField("Cохранить")
