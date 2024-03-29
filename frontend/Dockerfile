FROM python:3.8

COPY requirements.txt app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit","run"]

CMD ["streamlit_app.py"]
