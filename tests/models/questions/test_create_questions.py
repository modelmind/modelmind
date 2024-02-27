import pytest
from io import StringIO
from csv import DictReader
from typing import List
from modelmind.models.questions.schemas import ScaleQuestion

from modelmind.models.questions.transformations import create_questions_from_csv, Question


# A helper function to simulate csv.reader input from a string
def simulate_csv_input(data: str, auto_generate_ids: bool = False) -> List[Question]:
    csv_file = StringIO(data)
    csv_reader = DictReader(csv_file)
    return create_questions_from_csv(csv_reader, auto_generate_ids)


def test_create_questions_from_valid_csv():
    data = """id,type,category,text,options,display,multiple,shuffle,language,required,min,max,interval,low_label,high_label
1,choice,math,"What is 2+2?",2|4|6|8,radio,False,False,en,True,,,,,
2,text,science,"What is H2O?",,,,,en,True,,,,,
3,scale,satisfaction,"Rate your experience",,,,True,en,True,1,5,1,Low,High
"""
    questions = simulate_csv_input(data)
    assert len(questions) == 3
    assert questions[0].question.type == "choice"
    assert questions[1].question.type == "text"
    assert questions[2].question.type == "scale"
    assert questions[0].question.options == ["2", "4", "6", "8"]
    assert questions[2].question.min == 1
    assert questions[2].question.max == 5


def test_create_questions_from_invalid_csv():
    data = """id,type,category,text,options,display,multiple,shuffle,language,required,min,max,interval,low_label,high_label
4,invalid,unknown,"Is this a question?",,,,,,False,,,,,
"""
    with pytest.raises(ValueError):
        simulate_csv_input(data)


def test_create_questions_with_missing_fields():
    data = """id,type,category,text
1,choice,math,"What is 2+2?"
"""
    with pytest.raises(KeyError):
        simulate_csv_input(data)


def test_create_questions_from_csv_with_only_scale_questions():
    # Notice the removal of options, display, multiple, shuffle columns since they're irrelevant for scale questions
    data = """id,type,category,text,min,max,interval,low_label,high_label,language,required
1,scale,feedback,"How satisfied are you with our service?",1,10,1,Not Satisfied,Very Satisfied,en,True
2,scale,product,"Rate the quality of the product you received",1,5,0.5,Poor,Excellent,en,True
3,scale,support,"How helpful was our customer support?",1,5,1,Unhelpful,Extremely Helpful,en,True
"""
    questions = simulate_csv_input(data)
    assert len(questions) == 3
    assert all(isinstance(question.question, ScaleQuestion) for question in questions)
    assert questions[0].question.min == 1 and questions[0].question.max == 10 and questions[0].question.interval == 1
    assert questions[1].question.min == 1 and questions[1].question.max == 5 and questions[1].question.interval == 0.5
    assert questions[2].question.min == 1 and questions[2].question.max == 5 and questions[2].question.interval == 1
    assert questions[0].question.low_label == "Not Satisfied" and questions[0].question.high_label == "Very Satisfied"
    assert questions[1].question.low_label == "Poor" and questions[1].question.high_label == "Excellent"
    assert questions[2].question.low_label == "Unhelpful" and questions[2].question.high_label == "Extremely Helpful"


def test_create_questions_from_csv_with_auto_generated_ids():
    data = """type,category,text,options,display,multiple,shuffle,language,required,min,max,interval,low_label,high_label
choice,math,"What is 2+2?",2|4|6|8,radio,False,False,en,True,,,,,
text,science,"What is H2O?",,,,,en,True,,,,,
scale,satisfaction,"Rate your experience",,,,True,en,True,1,5,1,Low,High
"""
    questions = simulate_csv_input(data, auto_generate_ids=True)
    assert len(questions) == 3
    assert questions[0].id == "1"
    assert questions[1].id == "2"
    assert questions[2].id == "3"
