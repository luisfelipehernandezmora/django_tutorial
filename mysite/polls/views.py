from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader # Not needed anymore, was part of tutorial
from .models import Choice, Question
from django.http import Http404 # Try-except section
from django.db.models import F
from django.urls import reverse
from django.views import generic
    
class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name="latest_question_list"
    
    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.order_by(-"pub_date")[:5]
    
class DetailView(generic.DetailView):
    model=Question
    template_name="polls/detail.html"
    
class ResultsView(generic.DetailView):
    model=Question
    template_name="polls/results.html"

# def index(request):
#     latest_question_list=Question.objects.order_by("-pub_date")[:5]
#     # output=", ".join([q.question_text for q in latest_question_list])
#     # return(HttpResponse("Hello, world. You're at the polls index"))
#     # template=loader.get_template("polls/index.html")
#     context={
#         "latest_question_list":latest_question_list,
#     }
#     # return(HttpResponse(template.render(context,request)))
#     return render(request,"polls/index.html",context)
    
# def detail(request, question_id):
#     # try:
#     #     question=Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist, but if it is that good, go ahead and make it a poll ;)")
#     # context={"question":question}
#     # return render(request,"polls/detail.html",context)
#     question=get_object_or_404(Question,pk=question_id)
#     context={"question":question}
#     return render(request,"polls/detail.html",context) 
#     # return HttpResponse(f"You are looking at question {question_id}")

# def results(request, question_id):
#     # response="You are looking at the results of question"
#     # return HttpResponse(f"{response} {question_id}")
#     question=get_object_or_404(Question,pk=question_id)
#     return render(request,"polls/results.html",{"question":question})

def vote(request,question_id):
    # return HttpResponse(f"You're voting on question {question_id}")
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        context={"question":question,"error_message":"You didn't select a choice."}
        return render(request,"polls/detail.html",context)
    else:
        selected_choice.votes=F("votes") + 1
        selected_choice.save()
        #TIP!!!!!!: Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button. (...from django tutorial)
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))