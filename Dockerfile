# pythonの3.8.0をベースにする
FROM python:3.8.0

# linuxの環境設定
RUN apt-get update \
    && apt-get upgrade -y \
    # imageのサイズを小さくするためにキャッシュ削除
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # pipのアップデート
    && pip install --upgrade pip

# 作業ディレクトリの設定
WORKDIR /home

# 資材のコピー
COPY ./mnt/ ${PWD}

# pythonのパッケージをインストール
RUN pip install -r requirements.txt

# コンテナ側で開放するポートの指定
EXPOSE 5000

# コマンドの実行
CMD ["flask", "run"]

