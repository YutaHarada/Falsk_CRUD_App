"""フィクスチャの共有"""
import pytest

from apps.app import create_app, db

from apps.crud.models import User


# フィクスチャ関数の定義
@pytest.fixture
def fixture_app():
    # == セットアップ処理 ==
    # テスト用のコンフィグを指定
    app = create_app("testing")

    # DBの利用
    # アプリケーションコンテキストをスタックへプッシュ
    app.app_context().push()

    # テスト用DBのテーブルを作成
    with app.app_context():
        db.create_all()

    # テストの実行
    yield app

    # == クリーンナップ処理 ==
    # レコードの削除
    User.query.delete()
    # 削除処理をコミット
    db.session.commit()


# テストクライアントを作成
@pytest.fixture
def client(fixture_app):
    return fixture_app.test_client()
