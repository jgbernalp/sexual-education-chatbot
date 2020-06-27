import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import tensorflow_text
import json
import nltk
import simpleneighbors
from tqdm import tqdm
import time

model = hub.load(
    'https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3')


def extract_sentences_from_json(qas_json):
    all_sentences = []
    for data in qas_json['data']:
        for paragraph in data['paragraphs']:
            sentences = nltk.tokenize.sent_tokenize(paragraph['context'])
            all_sentences.extend(
                zip(sentences, [paragraph['context']] * len(sentences)))
    return list(set(all_sentences))  # remove duplicates


def extract_questions_from_json(qsa_json):
    questions = []
    for data in qsa_json['data']:
        for paragraph in data['paragraphs']:
            for qas in paragraph['qas']:
                if qas['answers']:
                    questions.append(
                        (qas['question'], qas['answers'][0]['text']))
    return list(set(questions))


def load_data_set(file_path):
    with open(file_path, 'r') as json_file_content:
        json_data = json.load(json_file_content)
        return json_data


def load_index(file_prefix):
    return simpleneighbors.SimpleNeighbors.load(file_prefix)


def train_model(file_path):
    nltk.download('punkt')

    questions_answers_json = load_data_set(file_path)
    print('Extracting answers and context from %s' % file_path)
    sentences = extract_sentences_from_json(questions_answers_json)
    # questions = extract_questions_from_json(questions_answers_json)

    print('Encoding sentences')
    encodings = model.signatures['response_encoder'](
        input=tf.constant([sentences[0][0]]),
        context=tf.constant([sentences[0][1]]))
    index = simpleneighbors.SimpleNeighbors(
        len(encodings['outputs'][0]), metric='angular')
    print('Computing embeddings for %s sentences' % len(sentences))

    batch_size = 100

    slices = zip(*(iter(sentences),) * batch_size)
    num_batches = int(len(sentences) / batch_size)
    for s in tqdm(slices, total=num_batches):
        response_batch = list([r for r, c in s])
        context_batch = list([c for r, c in s])
        encodings = model.signatures['response_encoder'](
            input=tf.constant(response_batch),
            context=tf.constant(context_batch)
        )
        for batch_index, batch in enumerate(response_batch):
            index.add_one(batch, encodings['outputs'][batch_index])

    index.build()
    print('simpleneighbors index for %s sentences built.' % len(sentences))
    timestr = time.strftime("%Y%m%d-%H%M%S")
    index.save('indexes/%s' % timestr)
    #  TODO Store this indexes in google cloud bucket


def get_answer(index, question, num_results=10):
    query_embedding = model.signatures['question_encoder'](
        tf.constant([question]))['outputs'][0]
    search_results = index.nearest(query_embedding, num_results)
    return search_results
