from django.shortcuts import render, HttpResponse
from surveillance.models import State
from django.conf import settings
from surveillance.ocr import ocr


def service(request):
    context_dict = {}
    states = State.objects.order_by('-time')[:5]
    context_dict['states'] = states
    return render(request, 'surveillance/service.html', context_dict)


def upload(request):
    if request.method == "POST":
        file = request.FILES['pic']

        fname = '%s/%s' % (settings.MEDIA_ROOT, file.name)
        with open(fname, 'wb') as pic:
            for c in file.chunks():
                pic.write(c)

        fname1 = './static/images/%s' % file.name
        with open(fname1, 'wb') as pic:
            for c in file.chunks():
                pic.write(c)

        data_list = ocr(fname)
        new_state = State.objects.create()
        new_state.liquid_level = data_list[0]
        new_state.temperature = data_list[1]
        new_state.high_set = data_list[2]
        new_state.low_set = data_list[3]
        new_state.save()
        return HttpResponse("Succeed!")
    else:
        return render(request, 'surveillance/upload.html')

