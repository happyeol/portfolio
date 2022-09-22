import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg # 기존 값 - 입력으로 받은 값

@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"] # 확장기능 nl2br : 줄바꿈 문자를 <br>로 변경, fenced_code : 마크다운의 소스코드 표현을 위해 필요
    return mark_safe(markdown.markdown(value, extensions=extensions)) # 마크다운 문법으로 작성한 문자열을 HTML로 변환함