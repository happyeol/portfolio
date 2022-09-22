from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm, Comment_QForm
from ..models import Question, Comment_Q

@login_required(login_url='common:login') # 로그인이 필요한 함수
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid(): # 폼이 유효하다면
            question = form.save(commit=False) # 임시 저장하여 question 객체를 리턴받는다.
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now() # 실제 저장을 위해 작성일시를 설정한다.
            question.save() # 데이터를 실제로 저장한다.
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form':form} # 1.폼이 유효하지 않거나, 2.질문 등록하기 버튼을 클릭한 경우
    return render(request, 'pybo/question_form.html', context) # 질문등록 화면을 보여줌

@login_required(login_url='common:login') # 로그인이 필요한 함수
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == 'POST':
        # 위에서 얻어온 question 객체에 POST 방식으로 전달된 data를 덮어씌워서 form 객체를 생성함
        # 수정된 내용으로 보여짐
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid(): # 폼이 유효하다면
            question = form.save(commit=False)
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        # GET 방식으로 요청된 경우 위에서 얻어온 question 객체로 form 객체를 생성함
        # 기존에 작성했던 내용 그대로 보여짐
        form = QuestionForm(instance=question)
    context = {'form':form} # 1.폼이 유효하지 않거나, 2.질문 등록하기 버튼을 클릭한 경우
    return render(request, 'pybo/question_form.html', context) # 질문등록 화면을 보여줌

@login_required(login_url='common:login') # 로그인이 필요한 함수
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login') # 로그인이 필요한 함수
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)

@login_required(login_url='common:login') # 로그인이 필요한 함수
def question_comment_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = Comment_QForm(request.POST)
        if form.is_valid():
            comment_q = form.save(commit=False)
            comment_q.author = request.user # author 속성에 로그인 계정 저장
            comment_q.create_date = timezone.now()
            comment_q.question = question
            comment_q.save()
            return redirect('pybo:detail', question_id=question.id)
    else: # method가 GET인 경우
        return redirect('pybo:detail', question_id=question.id)
    context = {'question':question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)