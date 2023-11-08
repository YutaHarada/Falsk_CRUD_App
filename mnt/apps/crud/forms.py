""" ユーザー新規登録・更新用のフォームクラス """

# import文
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, length


# ユーザー新規作成とユーザ更新のフォームクラス
class UserForm(FlaskForm):
    # ユーザーフォームのusername属性のラベルとバリデータを設定
    username = StringField(
        label="ユーザ名",
        validators=[
            DataRequired(message="ユーザ名は必須です。"),
            length(max=30, message="30文字以内で入力してください。")
        ]
    )

    # ユーザーフォームのemail属性のラベルとバリデータを設定
    email = StringField(
        label="メールアドレス",
        validators=[
            DataRequired(message="メールアドレスは必須です。"),
            Email(message="メールアドレスの形式で入力してください。")
        ]
    )

    # ユーザーフォームのpassward属性のラベルとバリデータを設定
    password = PasswordField(
        label="パスワード",
        validators=[
            DataRequired(message="パスワードは必須です。")
        ]
    )

    # ユーザーフォームのsubmit属性の文言を設定
    submit_add = SubmitField("ユーザー登録")
    submit_edit = SubmitField("更新")
    submit_delete = SubmitField("削除")
