from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from ..models import Question

def index(request):
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') # 검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) | # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw) # 답변 글쓴이 검색
        ).distinct() # 중복 제거
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list':page_obj, 'page':page, 'kw':kw} # question_list는 페이징 객체(page_obj)
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    page = request.GET.get('page', '1')  # 페이지
    sort = request.GET.get('sort', 'latest')  # 정렬
    question = get_object_or_404(Question, pk=question_id)
    if sort == 'latest':
        answer_list = question.answer_set.all().order_by('-create_date')
    else:
        answer_list = question.answer_set.all().annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
        # Count 인자로 ManytoMany 필드 객체를 전달할 수 있으며, 추천한 User 객체 수를 리턴함.
        # annotate : User 객체 수를 num_voter 변수로 바인딩(num_voter 라는 새로운 필드에 값을 대입했다고 생각하면 됨)
    paginator = Paginator(answer_list, 5)  # 페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question':question, 'answer_list':page_obj, 'page':page, 'sort':sort}
    return render(request, 'pybo/question_detail.html', context)