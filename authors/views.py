from django.shortcuts import render  # type: ignore

# Create your views here.


def register_view(request):
    return render(request, 'authors/pages/register_view.html')
