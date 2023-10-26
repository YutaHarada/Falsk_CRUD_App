""" ユーザー情報管理機能 """

# import文
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from apps.app import db
from apps.crud.models import User
from apps.crud.forms import UserForm

# crudアプリの生成
crud = Blueprint(
    name="crud",
    import_name=__name__,
    template_folder="templates"
)


# ===== ユーザー一覧機能のエンドポイント =====
@crud.route("/")
@login_required
def users():
    # ユーザーの一覧を取得
    users = User.query.all()
    return render_template("crud/users.html", users=users)


# ===== ユーザー作成機能のエンドポイント =====
@crud.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    # UserFormのインスタンス化
    form = UserForm()
    # formからサブミットされた場合は、ユーザーを作成しユーザーの一覧画面へリダイレクト
    if form.validate_on_submit():
        # ユーザ-を作成
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        # 追加内容をコミット
        db.session.add(user)
        db.session.commit()
        # ユーザーの一覧画面へリダイレクト
        return redirect(url_for("crud.users"))

    return render_template("crud/create.html", form=form)


# ===== ユーザー編集機能のエンドポイント =====
@crud.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    # UserFormのインスタンス化
    form = UserForm()
    # 更新対象ユーザーの情報を取得
    user = User.query.filter_by(id=user_id).first()
    # formからサブミットされた場合は、ユーザー情報を更新しユーザーの一覧画面へリダイレクト
    if form.validate_on_submit():
        # ユーザー情報を更新
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        # 更新内容をコミット
        db.session.add(user)
        db.session.commit()
        # ユーザーの一覧画面へリダイレクト
        return redirect(url_for("crud.users"))

    return render_template("crud/edit.html", user=user, form=form)


# ===== ユーザー削除機能のエンドポイント =====
@crud.route("user/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    # 削除対象ユーザーの情報の取得
    user = User.query.filter_by(id=user_id).first()
    # ユーザーを削除しコミット
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))
