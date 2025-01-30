FROM nikolaik/python-nodejs:python3.11-nodejs22-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn


COPY package.json package-lock.json* ./
RUN npm install && npm cache clean --force


COPY app app
COPY contacts.py config.py boot.sh ./
RUN chmod a+x boot.sh


RUN npm run build-styles

ENV FLASK_APP contacts.py
RUN flask


EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
