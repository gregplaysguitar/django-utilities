from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import Http404


def paginate(objects, per_page, p):
    """One-line pagination, which raises Http404 on invalid page number - example:

       >>> page = paginate(MyModel.objects.all(), 10, request.GET.get('p', 1))
    """
    paginator = Paginator(objects, per_page)

    try:
        p = int(p)
    except ValueError:
        raise Http404

    try:
        return paginator.page(p)
    except (EmptyPage, InvalidPage):
        raise Http404
