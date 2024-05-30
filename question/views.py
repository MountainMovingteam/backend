from django.shortcuts import render
import json
from mysite.lib.static_response import *
from .models import Question
from mysite.lib.static_fun import user_auth, question_json
import json


# Create your views here.

def create_question(request):
    data = json.loads(request.body.decode('utf-8'))

    type = data.get('type')

    content = json.loads(data.get('content'))
    A_content = content.get('a_option')
    B_content = content.get('b_option')
    C_content = content.get('c_option')
    D_content = content.get('d_option')
    answer = content.get('answer')
    title = data.get('title')

    Question.objects.create(title=title, A_content=A_content,
                            B_content=B_content, C_content=C_content,
                            D_content=D_content, answer=answer, type=type)

    return JsonResponse({'success': True})


def query_question(request):
    response = user_auth(request)

    if response is not None:
        return response

    data = json.loads(request.body.decode('utf-8'))

    question_num = data.get('question_num', None)

    if question_num is None:
        return necessary_content_is_none('question_num')

    ans = []
    for question in Question.objects.order_by('?')[:10]:
        ans.append(question_json(question))

    return JsonResponse({
        "list": ans
    })


def query_answer(request):
    response = user_auth(request)

    if response is not None:
        return response

    data = json.loads(request.body.decode('utf-8'))

    question_num = data.get('question_num', None)

    if question_num is None:
        return necessary_content_is_none('question_num')

    question_list = data.get('list', None)

    if question_list is None:
        return necessary_content_is_none('question_list')

    correct_num = 0

    res_list = []
    for each_question in question_list:
        correct = False
        question_id = json.loads(each_question).get('question_id')
        student_ans = json.loads(each_question).get('student_answer')

        question = Question.objects.filter(id=question_id)

        if question.answer == student_ans:
            correct = True
            correct_num = correct_num + 1

        res_list.append({
            'question_id': question_id,
            'correct': correct,
            'correct_ans': question.answer
        })

    return JsonResponse({
        'list': res_list,
        'correct_rate': correct_num / question_num
    })
