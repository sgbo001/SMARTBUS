from django.shortcuts import render
from .forms import SearchForm
# Create your views here.

    
def home(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            # Process the form data and perform the search logic
            from_post_code = form.cleaned_data['from_post_code']
            to_post_code = form.cleaned_data['to_post_code']
            date_time = form.cleaned_data['date_time']
            # Perform search logic and return results
    else:
        form = SearchForm()
    return render(request, 'home.html', {'form': form})

