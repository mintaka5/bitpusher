import hashlib
import os.path
import re
import time
from pathlib import Path

from nltk import word_tokenize, pos_tag, ne_chunk
from blitzdb import FileBackend, Document
from blitzdb.document import DoesNotExist
from nltk.corpus import stopwords
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import mark_negation


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
        the_message = re.sub("[^a-zA-Z0-9]", " ", message['message'])
        # split up sentence and train word entities
        tokens = word_tokenize(the_message)
        # remove 'stop' words (all too commonly used words)
        tokens = [w for w in tokens if w not in stopwords.words("english")]
        tokens_pos = pos_tag(tokens)
        tokens_tagged = ne_chunk(tokens_pos)
        related_hashes = message['correlations'];
        for token in tokens:
            # TODO : do this for phrases/sentences
            record_hash = store(token, db)
            related_hashes.append(record_hash)
            message['correlations'] = related_hashes
            message.save()
        db.commit()
    except DoesNotExist:
        print("fingerprint %s does not exist" % fingerprint)


def train(user_input, db):
    record_hash = store(user_input, db)
    learning(record_hash, db)


def process_input(user_input, db):
    if len(user_input) > 0:
        # train(user_input, db)
        print("user input: `%s`" % user_input)
        uin_tokens = word_tokenize(user_input, preserve_line=True)
        senti_analyzer = SentimentAnalyzer()
        all_words_neg = senti_analyzer.all_words([mark_negation(doc) for doc in uin_tokens])
        print(all_words_neg)


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
        else:
            if user_input == "purge":
                messages = db.filter(Message, {})
                messages.delete()
                db.commit()
