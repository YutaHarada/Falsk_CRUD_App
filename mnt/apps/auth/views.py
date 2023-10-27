""" 認証機能 """

# import文
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, logout_user

from apps.app import db
from apps.crud.models import User
from apps.auth.forms import SignUpForm, LoginForm

# authアプリの生成
auth = Blueprint(
    name="auth",
    import_name=__name__,
    template_folder="templates"
)


# ===== サインアップ画面のエンドポイント =====
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # SignUpFormのインスタンス化
    form = SignUpForm()
    # formからサブミットされた場合は、ユーザーを登録しユーザーの一覧画面へリダイレクト
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # メールアドレスの重複チェック
        if user.is_duplicate_email():
            flash("指定メールアドレスは登録済みです。")
            return redirect(url_for("auth.signup"))

        # 登録内容をコミット
        db.session.add(user)
        db.session.commit()
        # ユーザー情報をセッションに格納
        login_user(user)

        # 未ログイン時にログインが必要なページにアクセスした際の処理
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("crud.users")
        return redirect(next_)

    return render_template("auth/signup.html", form=form)


# ===== ログイン画面のエンドポイント =====
@auth.route("/login", methods=["GET", "POST"])
def login():
    # LoginFormのインスタンス化
    form = LoginForm()
    # formからサブミットされた場合は、ログイン処理をしユーザーの一覧画面へリダイレクト
    if form.validate_on_submit():
        # メールアドレスからユーザーを取得
        user = User.query.filter_by(email=form.email.data).first()

        # ユーザーが存在し、パスワードが一致する場合はログインを許可
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("crud.users"))

        # 上記条件を満たさなかった場合は、ログイン失敗メッセージを表示
        flash("メールアドレスかパスワードが不正です。")

    return render_template("auth/login.html", form=form)


# ===== ログアウトのエンドポイント =====
@auth.route("/logout")
def logout():
    # ログインセッションのリセット
    logout_user()
    # ログアウト後にログイン画面にリダイレクト
    return redirect(url_for("auth.login"))
