""" サインアップ・ログインのフォームクラス """

# import文
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


# サインアップ機能のフォームクラス
class SignUpForm(FlaskForm):
    username = StringField(
        label="ユーザ名",
        validators=[
            DataRequired(message="ユーザ名は必須です。"),
            Length(min=1, max=30, message="30文字以内で入力してください。")
        ]
    )
    email = StringField(
        label="メールアドレス",
        validators=[
            DataRequired(message="メールアドレスは必須です。"),
            Email(message="メールアドレスの形式で入力してください。")
        ]
    )
    password = PasswordField(
        label="パスワード",
        validators=[
            DataRequired(message="パスワードは必須です。")
        ]
    )
    submit = SubmitField("サインアップ")


# ログイン機能のフォームクラス
class LoginForm(FlaskForm):
    email = StringField(
        label="メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレスの形式で入力してください。")
        ]
    )
    password = PasswordField(
        label="パスワード",
        validators=[
            DataRequired("パスワードは必須です。")
        ])
    submit = SubmitField("ログイン")
