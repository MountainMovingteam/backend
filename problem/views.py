from django.shortcuts import render
from mysite.lib.static_fun import admin_auth
import json
from mysite.lib.static_response import *
from .models import Problem
from mysite.lib.static_fun import vector_match, user_auth


# Create your views here.


def create_problem(request):
    data = json.loads(request.body.decode('utf-8'))
    question = data.get("question")
    answer = data.get("answer")

    Problem.objects.create(question=question, answer=answer)

    return JsonResponse({
        'success': True
    })


def query_vague(request):
    response = user_auth(request)

    if response is not None:
        return response

    data = json.loads(request.body.decode('utf-8'))

    keywords = data.get('keywords', None)

    if keywords is None:
        return necessary_content_is_none('keywords')

    ans = []
    for problem in Problem.objects.all():
        if vector_match(problem.question, keywords):
            ans.append({
                "problem_id": problem.id,
                "content": problem.question
            })

    return JsonResponse({
        "list": ans,
        "num": len(ans)
    })


def query_ans(request):
    response = user_auth(request)

    if response is not None:
        return response

    data = json.loads(request.body.decode('utf-8'))

    problem_id = data.get("problem_id", None)

    if problem_id is None:
        return necessary_content_is_none('problem_id')

    problem = Problem.objects.filter(id=problem_id).first()

    if problem is None:
        return problem_id_not_exists()

    return JsonResponse({
        "answer": problem.answer
    })
