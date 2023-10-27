""" ユーザー情報管理モデル """

# import文
from datetime import datetime

from apps.app import db, login_manager

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# usersテーブルの作成
class User(db.Model, UserMixin):
    # テーブル名
    __tablename__ = "users"
    # カラム定義
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )

    # パスワードをセットするためのプロパティ
    @property
    def password(self):
        raise AttributeError("読み取り不可")

    # ハッシュ化したパスワードをセット
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)

    # パスワードをチェックする(ログイン機能で利用)
    # 入力されたパスワードがDBのハッシュ化されたパスワードと一致するかをチェックし、一致する場合はTrueを返す
    def verify_password(self, password):
        return check_password_hash(
            pwhash=self.password_hash,
            password=password
        )

    # メールアドレス重複チェックをする(サインアップ機能で利用)
    # 入力されたメールアドレスがDBに存在する場合はTrueを返す
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None


# flask_login拡張機能がログインしているユーザー情報を取得するために利用する
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
