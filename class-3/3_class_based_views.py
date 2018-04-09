[docs](https://docs.djangoproject.com/en/2.0/topics/class-based-views/)

##### 1. Refactor index view using a TemplateView

```python
from django.views.generic import TemplateView

class IndexPageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coins = Cryptocurrency.objects.all().order_by('rank')
        context['coins'] = coins
        return context
```

##### 2. Refactor create to be a form view

```python
from django.views.generic.edit import FormView

class CreateCryptoView(FormView):
    template_name = 'create.html'
    form_class = CryptocurrencyForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
```

Show that it can be accessed by not-authenticated users.

##### 3. Add the method decorator

```python
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class CreateCryptoView(FormView):
    template_name = 'create.html'
    form_class = CryptocurrencyForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
```

##### 4. Use the LoginRequiredMixin

```python
from django.contrib.auth.mixins import LoginRequiredMixin
class CreateCryptoView(LoginRequiredMixin, FormView):
    template_name = 'create.html'
    form_class = CryptocurrencyForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
```

##### 5. Refactor the FormView to CreateView

[docs](https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-editing/#model-forms)

```python
from django.views.generic.edit import CreateView

class CreateCryptoView(LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    form_class = CryptocurrencyForm
    success_url = '/'
```

##### 6. Add Django Messages

```python
from django.contrib import messages

class CreateCryptoView(LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    form_class = CryptocurrencyForm
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, "Your crypto was created!")
        return super().form_valid(form)

```

##### 7. Include Django Braces FormValidMessageMixin

```python
from braces.views import FormValidMessageMixin

class CreateCryptoView(LoginRequiredMixin, FormValidMessageMixin, CreateView):
    template_name = 'create.html'
    form_class = CryptocurrencyForm
    success_url = '/'
    # form_valid_message = "Your crypto was created!"

    def get_form_valid_message(self):
        return "Crypto {} created!".format(self.object.name)
```
