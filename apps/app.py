""" Flaskアプリの管理/起動 """

# import文
from apps.config import config

import logging

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager

# SQLAlchemyをインスタンス化
db = SQLAlchemy()
# CSRF対策を施すためのCSRFProtectクラスのインスタンス化
csrf = CSRFProtect()
# LoginManagerをインスタンス化
login_manager = LoginManager()
# login_view属性に未ログイン時にリダイレクトするエンドポイントを指定する。
login_manager.login_view = "auth.login"
# login_message属性にログイン後に表示するメッセージを指定する。
login_manager.login_message = ""


# アプリ構築用関数を定義
def create_app(config_key):
    # Flaskインスタンスの生成
    app = Flask(__name__)

    # config_keyに応じた環境のコンフィグクラスを読み込む
    app.config.from_object(config[config_key])

    # ログレベルの設定
    app.logger.setLevel(logging.DEBUG)

    # CSRFProtectとアプリの連携
    csrf.init_app(app)
    # SQLAlchemyとアプリの連携
    db.init_app(app)
    # Migrateとアプリの連携
    Migrate(app, db)
    # login_managerをアプリの連携
    login_manager.init_app(app)

    # crudパッケージからviewsをimportする。
    from apps.crud import views as crud_views
    # authパッケージからviewsをimportする。
    from apps.auth import views as auth_views

    # register_blueprintを用いてviewsのcrud,auth,dt(detector)をアプリへ登録する。
    app.register_blueprint(blueprint=crud_views.crud, url_prefix="/")
    app.register_blueprint(blueprint=auth_views.auth, url_prefix="/auth")

    return app
