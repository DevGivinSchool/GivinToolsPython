from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def index(request):
    return HttpResponse('ok')


def my_view(request):
    # t = loader.get_template('gtp_index/index.html')
    # context = {'foo': 'bar'}
    # return HttpResponse(t.render(context, request))
    return render(request, 'index.html', context={'foo': 'bar'})
