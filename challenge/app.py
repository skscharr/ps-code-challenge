import csv
import os
from flask import Flask

from challenge.api import QuestionAPI
from challenge.database import init_db, db_session, Question

APP = Flask(__name__)
init_db()


def populate_database(session):
    """
    Populate the in memory database with data from the
    provided CSV file code_challenge_question_dump.csv
    """
    q_dump = 'code_challenge_question_dump.csv'
    q_dump_location = '/'.join([os.path.dirname(os.path.realpath(__file__)), q_dump])
    with open(q_dump_location, 'r') as f:
        csv_reader = csv.reader(f, delimiter='|')
        for row in csv_reader:
            if row[0] == "question":
                # skip the header row
                continue
            session.add(Question(question=row[0], answer=row[1], distractors=row[2]))
        session.commit()

populate_database(db_session)

question_view = QuestionAPI.as_view('questions')
APP.add_url_rule(
    '/questions',
    defaults={'qid': None},
    view_func=question_view,
    methods=['GET',])
APP.add_url_rule(
    '/questions',
    view_func=question_view,
    methods=['POST',])
APP.add_url_rule(
    '/questions/<int:qid>',
    view_func=question_view,
    methods=['GET', 'PUT', 'DELETE',])


@APP.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
