from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def paginate_profiles(request, pr, result):
    page = request.GET.get('page')
    # result = 4
    paginator = Paginator(pr, result)

    try:
        pr = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        pr = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        pr = paginator.page(page)

    left_index = int(page) - 4

    if left_index < 1:
        left_index = 1

    right_index = int(page) + 5

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)
    return custom_range, pr


def search_profiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__iexact=search_query)  # iexact точное совпадение без учета регистра

    prof = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_info__icontains=search_query) |
        Q(skill__in=skills)
    )
    return prof, search_query
