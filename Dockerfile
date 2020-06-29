FROM tensorflow/tensorflow

RUN pip install flask
RUN pip install tensorflow_text
RUN pip install tensorflow
RUN pip install tensorflow_hub
RUN pip install simpleneighbors[annoy]

WORKDIR /usr/app
COPY . ./

CMD ["python", "app.py"]