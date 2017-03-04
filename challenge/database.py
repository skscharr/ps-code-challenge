from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite://')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    distractors = Column(String)

    def __repr__(self):
        return (
            "<Question(question='{}', answer={}, "
            "distractors={})>".format(
                self.question, self.answer, self.distractors))


def init_db():
    Base.metadata.create_all(bind=engine)
