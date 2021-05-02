  
FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./
EXPOSE 5000/tcp
# CMD ["python", './app.py']
CMD python ./app.py
# CMD python ./script.py ; python ./app.py