# ベースイメージを選択
FROM continuumio/miniconda3

# パッケージを更新
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8501

RUN conda update -n base -c defaults conda

# ローカルのenv.ymlファイルをコンテナにコピー
COPY ./env.yml /tmp/env.yml

# condaの環境を作成
RUN conda env create -f /tmp/env.yml

# activate myenv
ENV CONDA_DEFAULT_ENV ResponseRecorder

# env setting(こちらはコンテナに入った時のため)
RUN echo "conda activate ResponseRecorder" >> ~/.bashrc
ENV PATH /opt/conda/envs/ResponseRecorder/bin:$PATH

WORKDIR /app