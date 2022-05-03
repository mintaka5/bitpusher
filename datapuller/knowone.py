import hashlib
import os.path
import re
import time
from pathlib import Path

import nltk
from blitzdb import FileBackend, Document
from blitzdb.document import DoesNotExist
from nltk import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords


class Message(Document):
    pass


def store(user_input, db):
    record_hash = hashlib.sha256(user_input.encode('utf8')).hexdigest()
    ts = time.time()

    try:
        message = db.get(Message, {'fingerprint': record_hash})
        # increment existing message's weight
        message.weight += 1
        message.save()

    except DoesNotExist:
        # insert a new record
        msg_record = Message({
            'fingerprint': record_hash,
            'timestamp': ts,
            'message': user_input,
            'weight': 0,
            'correlations': []
        })
        db.save(msg_record)
    db.commit()

    return record_hash


def learning(fingerprint, db):
    try:
        message = db.get(Message, {'fingerprint': fingerprint})
        # normalize: remove all punctuation
        the_message = re.sub("[^a-zA-Z0-9]", " ", message['message'].lower())
        # split up sentence and train word entities
        tokens = nltk.word_tokenize(the_message)
        print(tokens)
        # remove 'stop' words (all too commonly used words)
        tokens = [w for w in tokens if w not in stopwords.words("english")]
        tokens_pos = nltk.pos_tag(tokens)
        tokens_tagged = nltk.ne_chunk(tokens_pos)
        print(tokens)
        # stemming & lemming
        # reduce words to stems
        stemmed = [PorterStemmer().stem(w) for w in tokens]
        print(stemmed)
        lemmed = [WordNetLemmatizer().lemmatize(w, pos='v') for w in stemmed]
        print(lemmed)

    except DoesNotExist:
        print("fingerprint %s does not exist" % fingerprint)


def train(user_input, db):
    record_hash = store(user_input, db)
    learning(record_hash, db)


def process_input(user_input, db):
    if len(user_input) > 0:
        train(user_input, db)


def boot_up():
    user_home_dir = os.path.expanduser("~")
    data_path = Path(user_home_dir, '.bitpusher', 'db')

    db = FileBackend(data_path)

    user_input = ""
    while user_input != "bye":
        user_input = input(">> ")

        # do not learn these commands
        commands = ['bye', 'purge', 'list', 'ls', 'exit']
        if user_input not in commands:
            process_input(user_input.strip(), db)
