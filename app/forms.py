from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Usuário", validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Senha", validators=[DataRequired(), Length(min=6, max=128)]
    )
    password2 = PasswordField(
        "Confirmar Senha",
        validators=[DataRequired(), EqualTo("password")],
    )
    submit = SubmitField("Registrar")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Este usuário já está em uso.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Este email já está cadastrado.")


class TaskForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Descrição", validators=[Length(max=2000)])
    completed = BooleanField("Concluída")
    submit = SubmitField("Salvar")
