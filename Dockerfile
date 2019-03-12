FROM python:3.7.2-alpine3.9

COPY crontab /etc/cron/crontab
RUN crontab /etc/cron/crontab

RUN apk --no-cache add ca-certificates \
		firefox-esr \
		tzdata \
		wget

RUN cd /tmp \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz \
    && tar xvfz geckodriver-v0.23.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin \
    && rm geckodriver-v0.23.0-linux64.tar.gz

ADD requirements.txt /usr/local
RUN pip3 install -r /usr/local/requirements.txt

COPY main.py /usr/local
WORKDIR /usr/local

ENV TZ="Europe/Berlin" \
    POSTBANKURL="https://postbank.de" \
    PICTUREPATH="/usr/local" \
    USERNAME="user" \
    PASSWORD="pass" \
    TELEGRAMBOTKEY="bot4711" \
    CHATID=4711

#CMD ["python3", "main.py"]
CMD ["crond", "-f"]