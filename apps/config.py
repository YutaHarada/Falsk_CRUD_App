""" Flaskのconfig設定 """

# import文
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# トップディレクトリ
basedir = Path(__file__).parent.parent


# 基本となるコンフィグの設定
class BaseConfig:
    # Cookieを暗号化するための秘密鍵
    SECRET_KEY = os.getenv("SECRET_KEY")
    # CSR対策を実施するための秘密鍵
    WTF_CSRF_SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY")


# 開発環境用のコンフィグ設定用クラス
class DevelopConfig(BaseConfig):
    # SQLiteのデータベースファイルを出力するパスを指定する。
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'develop.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLをコンソールログに出力する設定
    SQLALCHEMY_ECHO = True


# 検証環境用のコンフィグ設定用クラス
class StagingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'staging.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# マッピング
config = {
    "testing": StagingConfig,
    "local": DevelopConfig
    }
