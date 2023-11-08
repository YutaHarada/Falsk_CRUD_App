
# ===== 未ログイン時のユーザー一覧画面のテスト =====
def test_index(client):
    rv = client.get("/", follow_redirects=True)
    # "ログイン"の文言が画面上にあるかを確認
    assert "ログイン" in rv.data.decode()
    # "サインアップ"の文言が画面上にあるかを確認
    assert "サインアップ" in rv.data.decode()


# ===== ログイン時のユーザー一覧画面のテスト =====
def signup(client, username, email, password):
    # サインアップを実行するために必要な情報を取得し、リクエストを実行
    data = dict(username=username, email=email, password=password)
    return client.post("/auth/signup", data=data, follow_redirects=True)


def test_index_signup(client):
    # サインアップの実行
    rv = signup(client, "admin", "test@example.com", "password")
    # ログインユーザがナビゲーションバーに表示されるかどうかの確認
    assert "admin" in rv.data.decode()

    rv = client.get("/", follow_redirects=True)
    assert "ログアウト" in rv.data.decode()
    assert "ユーザー新規作成" in rv.data.decode()
