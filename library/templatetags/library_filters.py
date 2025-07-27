from django.db.models import Sum
from django import template

register = template.Library()

@register.filter
def calculate_total_score(user):
    return user.score_entries.aggregate(Sum('score'))['score__sum'] or 0
