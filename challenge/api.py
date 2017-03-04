from flask import jsonify, request
from flask.views import MethodView
from werkzeug import exceptions

from challenge.database import db_session, Question


class QuestionAPI(MethodView):

    def get(self, qid=None):
        """
        Get all or a single question

        :param int qid: The question ID. If None, return all
            questions
        """
        if qid:
            Q = Question.query.get(qid)
            return jsonify({
                'question': Q.question,
                'answer': Q.answer,
                'distractors': Q.distractors.split(',')
            }), 200

        response = {'questions': []}
        for Q in Question.query.all():
            response['questions'].append({
                'question': Q.question,
                'answer': Q.answer,
                'distractors': Q.distractors.split(',')
            })

        return jsonify(response), 200

    def post(self):
        """
        Create a new multiple choice question

        :reqjson str question: A question
        :reqjson str answer: The answer to the question
        :reqjson list distractors: A list of fake answers
        """
        data = request.json
        _validate_question_request(data)

        db_session.add(Question(
            question=data.get('question'),
            answer=data.get('answer'),
            distractors=','.join(data.get('distractors', []))))
        db_session.commit()

        return jsonify({'ok': True}), 201

    def put(self, qid):
        """
        Edit an existing question

        :param int qid: The question ID
        :reqjson str question: A question
        :reqjson str answer: The answer to the question
        :reqjson list distractors: A list of fake answers
        """
        data = request.json
        _validate_question_request(data)

        Q = Question.query.get(qid)
        Q.question = data.get('question')
        Q.answer = data.get('answer')
        Q.distractors = ','.join(data.get('distractors', []))

        db_session.commit()

        return jsonify({'ok': True}), 202

    def delete(self, qid):
        """
        Delete a question

        :param int qid: The question ID
        """
        Q = Question.query.get(qid)
        db_session.delete(Q)
        return jsonify({'ok': True}), 200

def _validate_question_request(data):
    """
    Validate the request data received for creating and editing
    questions.
    """
    if not data or data.get('question') is None or data.get('answer') is None:
        raise exceptions.BadRequest(description='Missing request data!')
    if not isinstance(list, data.get('distractors', [])):
        raise exceptions.BadRequest(description='"distractors" must be a list!')
