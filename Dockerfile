FROM python:3

WORKDIR /api

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /api

CMD [ "python", "api/app.py" ]