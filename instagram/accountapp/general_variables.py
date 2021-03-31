from .forms import SearchForm

def variable_general(request):
    form = SearchForm()
    to_temp = {'s_form': form, 'name':'Jerry'}
    return to_temp
