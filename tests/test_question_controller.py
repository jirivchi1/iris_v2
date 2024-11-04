# test_question_controller.py
from app.controllers.question_controller import handle_questions_and_responses


def test_handle_questions_and_responses():
    # Test data
    user_name = "test_user"
    age = "30"
    career_profession = "Engineer"
    question_1 = "What do you see in the image?"
    question_2 = "Describe the number of objects in the image."
    image_path_1 = "static/images/test/4_renos.png"
    image_path_2 = "static/images/test/uvas.jpg"

    response_1, response_2 = handle_questions_and_responses(
        user_name,
        age,
        career_profession,
        question_1,
        question_2,
        image_path_1,
        image_path_2,
    )

    print("Response 1:", response_1)
    print("Response 2:", response_2)


if __name__ == "__main__":
    test_handle_questions_and_responses()
