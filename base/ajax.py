from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from base.data import data

# @login_required
@require_http_methods(["GET"])
def filter_result(request):
    # query = request.GET.get('search', '')
    # kwargs = {
    #     'is_active': True,
    #     'profile__role__in': [1, 3],
    # }
    # if query:
    #     qset = (
    #             Q(username__icontains=query) |
    #             Q(first_name__icontains=query) |
    #             Q(last_name__icontains=query)
    #     )
    #     clients = User.objects.filter(qset, **kwargs)
    # else:
    #     clients = User.objects.filter(**kwargs)
    #
    # results = [{'id': i.pk, 'text': i.username} for i in clients]
    return JsonResponse({"results": data}, safe=False)