from typing import Any, Dict, Iterator, List, Literal, Union, cast

from pydantic_core import ValidationError

from modelmind.models.questions.schemas import ChoiceQuestion, Question, ScaleQuestion, TextQuestion


def create_question_from_dict(question_data: Dict[str, Any]) -> Question:
    question_type = question_data["type"]
    question: Union[ChoiceQuestion, TextQuestion, ScaleQuestion]
    if question_type == "choice":
        question_data["options"] = (
            question_data["options"].split("|")
            if isinstance(question_data["options"], str)
            else question_data.get("options", [])
        )
        question = ChoiceQuestion.model_validate(question_data)
    elif question_type == "text":
        question = TextQuestion.model_validate(question_data)
    elif question_type == "scale":
        question = ScaleQuestion.model_validate(question_data)
    else:
        raise ValueError("Invalid question type")
    return Question.model_validate({**question_data, "question": question.model_dump()})


def create_question_from_string_dict(question_data: Dict[str, str]) -> Question:
    try:
        question: Union[ChoiceQuestion, TextQuestion, ScaleQuestion]
        question_type = question_data["type"]

        if question_type == "choice":
            question = ChoiceQuestion(
                type="choice",
                text=question_data["text"],
                multiple=question_data.get("multiple", "False").lower() == "true",
                display=cast(Literal["radio", "checkbox", "dropdown"], question_data["display"]),
                options=question_data["options"].split("|"),  # Assuming options are separated by '|'
                shuffle=question_data.get("shuffle", "False").lower() == "true",
            )
        elif question_type == "text":
            question = TextQuestion(type="text", text=question_data["text"])
        elif question_type == "scale":
            question = ScaleQuestion(
                type="scale",
                text=question_data["text"],
                min=int(question_data["min"]),
                max=int(question_data["max"]),
                interval=float(question_data["interval"]),
                low_label=question_data["low_label"],
                high_label=question_data["high_label"],
                shuffle=question_data.get("shuffle", "False").lower() == "true",
            )
        else:
            raise ValueError(f"Invalid question type: {question_type} from {question_data}")

        # Return the instantiated Question object
        return Question(
            id=question_data["id"],
            category=question_data["category"],
            question=question,
            language=question_data["language"],
            required=question_data.get("required", "True").lower() == "true",
        )

    except ValidationError as e:
        print(f"Error validating question: {e}")
        raise e


def create_questions_from_csv(
    csv_reader: Iterator, auto_generate_ids: bool = False, ignore_invalid: bool = False
) -> List[Question]:
    questions = []

    auto_id = 1

    for row in csv_reader:
        if auto_generate_ids:
            row["id"] = str(auto_id)
            auto_id += 1

        try:
            question = create_question_from_string_dict(row)
            if question:
                questions.append(question)
        except Exception as e:
            if not ignore_invalid:
                raise e
            print(f"Error creating question: {e}")
            auto_id -= 1

    return questions
