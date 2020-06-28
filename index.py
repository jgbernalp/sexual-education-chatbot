import tensorflow.compat.v2 as tf
import tensorflow_text
import tensorflow_hub as hub
import simpleneighbors

model = hub.load(
    'https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3')


def load_index(file_prefix):
    return simpleneighbors.SimpleNeighbors.load(file_prefix)


def get_answer(index, question, num_results=3):
    query_embedding = model.signatures['question_encoder'](
        tf.constant([question]))['outputs'][0]
    search_results = index.nearest(query_embedding, num_results)
    return search_results
