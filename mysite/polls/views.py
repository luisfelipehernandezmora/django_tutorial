from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader # Not needed anymore, was part of tutorial
from .models import Question
from django.http import Http404 # Try-except section

def index(request):
    latest_question_list=Question.objects.order_by("-pub_date")[:5]
    # output=", ".join([q.question_text for q in latest_question_list])
    # return(HttpResponse("Hello, world. You're at the polls index"))
    # template=loader.get_template("polls/index.html")
    context={
        "latest_question_list":latest_question_list,
    }
    # return(HttpResponse(template.render(context,request)))
    return render(request,"polls/index.html",context)

def detail(request, question_id):
    try:
        question=Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist, but if it is that good, go ahead and make it a poll ;)")
    
    context={"question":question}
    return render(request,"polls/detail.html",context)
    
    
    
    
    return HttpResponse(f"You are looking at question {question_id}")

def results(request, question_id):
    response="You are looking at the results of question"
    return HttpResponse(f"{response} {question_id}")

def vote(request,question_id):
    return HttpResponse(f"You're voting on question {question_id}")