FROM tensorflow/tensorflow

RUN pip install flask
RUN pip install tensorflow_text
RUN pip install tensorflow
RUN pip install tensorflow_hub
RUN pip install simpleneighbors[annoy]
RUN pip install numpy
RUN pip install tqdm
RUN pip install nltk

WORKDIR /usr/app
COPY . ./

CMD ["python", "app.py"]