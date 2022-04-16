import hashlib
import os
import time
from pathlib import Path

import nltk
from nltk.corpus import sentiwordnet
from tinydb import TinyDB, Query
from tinydb.operations import increment


def clear_screen():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')


def store(uin, db: TinyDB) -> str:
    record_hash = hashlib.sha256(uin.encode('utf8')).hexdigest()
    ts = time.time()

    record_exists = db.get(Query().fingerprint == record_hash)

    if record_exists is None:
        # insert new unique message
        db.insert({'fingerprint': record_hash, 'timestamp': ts, 'message': uin, 'weight': 0})
    else:
        # or increment the weight of an existing unique message
        record_hash = record_exists.get('fingerprint')
        db.update(increment('weight'), Query().fingerprint == record_hash)

    return record_hash


def learning(record_hash, db):
    recs = db.all()
    txt = ' '.join("%s" % ''.join(map(str, x.get('message'))) for x in recs)

    # get tags for POS
    tokens = nltk.word_tokenize(txt)
    pos_tags = nltk.pos_tag(tokens)
    # [print(tag) for tag in pos_tags]


def train(user_input, db: TinyDB):
    record_hash = store(user_input, db)
    learning(record_hash, db)


def purge_all(db: TinyDB):
    db.truncate()


def process_user_input(user_input: str, db: TinyDB):
    if len(user_input) > 0:
        # train(user_input, db)
        # response
        tokens = nltk.word_tokenize(user_input)
        tags = nltk.pos_tag(tokens)
        # find entities
        # entities = nltk.chunk.ne_chunk(tags)
        [print(list(sentiwordnet.senti_synsets(tag[0], tag[1].lower()))) for tag in tags]
        # print(tags)
        # print(entities)


def list_records(db):
    res = db.all()
    # sort by date
    sorted(res, key=lambda x: x.get('timestamp'))
    # flip it around to get most recent first
    # res.reverse()

    [
        print(
            "[%s] %s: %s" % (
                time.strftime("%Y-%m-%d %H:%M:%S",
                              time.gmtime(rec.get('timestamp'))),
                rec.get('fingerprint'),
                rec.get('message'))
        ) for rec in res
    ]


def boot_up():
    # create storage JSON file if not exists
    user_home_dir = os.path.expanduser("~")
    bitpusher_json_path = Path(user_home_dir, '.bitpusher', 'stow.json')

    if not bitpusher_json_path.exists():
        # create file and relevant parent directories
        bitpusher_json_path.parent.mkdir(exist_ok=True, parents=True)
        bitpusher_json_path.touch()

    # establish database
    db = TinyDB(bitpusher_json_path)

    uin = ""
    while uin != "bye":
        # user input
        uin = input(">> ")

        # do not record these commands
        commands = ['bye', 'purge', 'list']
        if uin not in commands:
            process_user_input(uin.strip(), db)
        else:
            if uin == "purge":
                db.truncate()
            elif uin == "list":
                list_records(db)

