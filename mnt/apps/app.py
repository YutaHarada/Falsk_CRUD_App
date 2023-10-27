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

# ロガーの設定
logging.basicConfig(filename='werkzeug.log', level=logging.DEBUG)
# Werkzeugのロガーを取得
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)
# ファイルハンドラを作成
file_handler = logging.FileHandler('werkzeug.log')
file_handler.setLevel(logging.DEBUG)
# フォーマッタを作成してハンドラにセット
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
file_handler.setFormatter(formatter)
# ハンドラをロガーに追加
werkzeug_logger.addHandler(file_handler)


# アプリ構築用関数を定義
def create_app(config_key):
    # Flaskインスタンスの生成
    app = Flask(__name__)

    # config_keyに応じた環境のコンフィグクラスを読み込む
    app.config.from_object(config[config_key])

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
