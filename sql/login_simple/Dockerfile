FROM python

COPY app /usr/src/app/
WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP="main"

# Save commands to initialize database and run webapp into a script that can be run after the db is up and running
RUN echo "python db.py" "&&" "flask run --host 0.0.0.0 --port 8000" > "run.sh"
RUN chmod u+x run.sh

CMD ["/bin/bash", "run.sh"]
