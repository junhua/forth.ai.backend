 FROM python:2.7
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
 ADD . /code/
