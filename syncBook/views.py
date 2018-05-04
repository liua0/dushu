from django.shortcuts import render

# Create your views here.
def test(request):
    context = {
        'd': dir(request)
    }
    return render(request, 'add_book.html', context=context)

