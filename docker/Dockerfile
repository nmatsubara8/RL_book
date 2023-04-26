FROM tensorflow/tensorflow:1.13.1-py3-jupyter

# Linuxパッケージのインストール
RUN apt-get update && apt-get install -y \
    git \
    autoconf \
    tmux \
    vim \
    wget \
    cmake \
    byobu \
    language-pack-ja \
    unzip \
    nscd \
    graphviz \
    libgtk2.0-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    protobuf-compiler \
    python-tk \
    python-pil \
    python-lxml \
    python-opengl \
    xvfb \
    ffmpeg  \
    && apt-get -y clean all \
    && rm -rf /var/lib/apt/lists/*

# 言語設定
RUN locale-gen ja_JP.UTF-8
ENV LANGUAGE ja_JP:en
ENV LC_ALL ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
RUN update-locale LANG=$LANG

# Pythonライブラリのインストール
RUN pip3 install --upgrade pip
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/

# pybullet-gymのインストール
RUN git clone https://github.com/benelot/pybullet-gym
RUN cd pybullet-gym \
&& pip install -e .

# Tensorboardのポート番号
EXPOSE 6006

# Jupyter Notebookのポート番号
EXPOSE 8888
