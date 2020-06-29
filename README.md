## installation

- Install python 2.7 in your local machine
- Navigate into the project folder

```
cd {your path}/chatbot-mvp
```

- Use a virtual environment

```
pip install virtualenv
virtualenv --version
virtualenv venv
```

- Activate the virtual environment

```
source venv/bin/activate
```

- Install the dependencies

```
pip install -r requirements.txt
```

## To run the server locally

Activate your virtual environment and run

```
python app.py
```

This will run the server in `localhost:8080`, it will use the `indexes/runtime.idx` and `indexes/runtime-data.pkl` to answer the questions provided in the frontend.

## To build the index locally

Make sure you have a `questions_answers.json` file in the root of your project.

Activate your virtual environment and run

```
python bootstrap_train.py
```

This will run build the index based on the `questions_answers.json` file, the index will be stored in the `indexes` folder.

## To use a new index

Run the previous step to build a new index and replace the index files as follows

```
index_{date}.idx -> index.idx
index_{date}-data.idx -> index-data.plk
```

## Troubleshooting

The index build script might get stuck while `encoding sentences` or `computing embedidngs`, this is an indication that you are not using the proper interpreter (python 2.7). Make sure you are using the interpreter provided by the virtual environment and not the one on your system.
