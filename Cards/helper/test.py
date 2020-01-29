from Cards.models import Question, TestQuestion, Test, QuestionLog


def create_new_test(user, course):
    test = Test()
    test.user = user
    test.course = course
    test.save()

    questions = Question.objects.filter(course=course).all()
    test_questions = []
    for q in questions:
        tq = TestQuestion()
        tq.test = test
        tq.question = q
        test_questions.append(tq)

    TestQuestion.objects.bulk_create(test_questions)

    return test


def finish_test_question(user, tq, type):
    log = QuestionLog()
    log.user = user
    log.question = tq.question
    log.type = type
    log.save()

    tq.type = type
    tq.save()
