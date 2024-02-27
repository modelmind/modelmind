import pytest
from io import StringIO
from csv import DictReader
from typing import List

from modelmind.models.questions.transformations import create_questions_from_csv, Question


# A helper function to simulate csv.reader input from a string
def simulate_csv_input(data: str) -> List[Question]:
    csv_file = StringIO(data)
    csv_reader = DictReader(csv_file)
    return create_questions_from_csv(csv_reader)


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
