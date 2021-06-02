from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def do_pagination(objects_set, col, request):
    paginator = Paginator(objects_set, col)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        objects = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        objects = paginator.page(paginator.num_pages)
    return objects, page
