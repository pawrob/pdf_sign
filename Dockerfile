FROM python:3.8

ENV FLASK_APP "app.py"
WORKDIR /app

RUN wget http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.16.tar.gz \
    && tar -xvzf libiconv-1.16.tar.gz \
    && cd libiconv-1.16 \
    && ./configure --prefix=/usr/local/lib \
    && make \
    && make install \
    && cd /usr/local/lib \
    && ln -s lib/libiconv.so libiconv.so \
    && ln -s libpython3.8.so.1.0 libpython.so \
    && ln -s lib/libiconv.so.2 libiconv.so.2

RUN apt-get update && apt-get install -y swig vim


RUN pip install  flask endesive cryptography
COPY . .
COPY . .

RUN useradd -ms /bin/bash  flask
RUN chown -R flask:flask /app
RUN chmod 777 /app
USER flask

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]