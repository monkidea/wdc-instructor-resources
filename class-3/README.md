# Class 3 - Advanced Topics

This class extends the previous marketcap project. The topics to cover are:

1. Template Inheritance
2. Basic static file conf
3. Using Class Based Views
4. Include a signal to create a Profile object with every new user
5. Add a favorite coin M2M file to profile and using AJAX to mark coins as favorite

# 1 - Template inheritance

_(this code is already provided)_

* Show repeated templates in previous project
* Explain base.html + blocks with index.html
* Explain `{% include %}` templatetag.

---

# 2 - Profile and static
**[More Details](/2_profile_static_files.md)**

---

# 3 - Class based views

**[More Details](/class_based_views.md)**

---

# 4 - Signals

##### 1 - Creation
Demonstrate how signals work by hooking up one for the User's model. In `models.py` (below profile):

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


@receiver(post_save, sender=get_user_model())
def create_profile_for_user(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

##### 2 - Refactor to signals.py

1. Create a module `cryptocoins/signals.py` and move the code there.
2. In `cryptocoins/apps.py`, define a method `ready` inside `CryptocoinsConfig`:
```python
def ready(self):
    from . import signals
```
3. In `settings.INSTALLED_APPS`, change `'cryptocoins'` for `'cryptocoins.apps.CryptocoinsConfig'`.

---

# 5 - Favorite Coins - Many to Many

##### 1. Many To Many field
Include a favorite_coins field in the `Profile` model.

```python
favorite_coins = models.ManyToManyField(Cryptocurrency)
```

**Make and Run migrations**

##### 2. Select a couple of coins as favorites and show shell

Use the shell + admin to demonstrate it:

```python
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(id=1)
>>> user.profile
>>> user.profile.favorite_coins.all()

>>> # Add coins:
>>> from cryptocoins.models import Cryptocurrency
>>> c = Cryptocurrency.objects.get(symbol='TRX')
>>> user.profile.favorite_coins.add(c)
>>> user.profile.favorite_coins.all()
```

##### 3. Include Favorite coins in view

The code for the view:
```python
favorite_coins = []
if self.request.user.is_authenticated:
    favorite_coins = self.request.user.profile.favorite_coins.all()
context['favorite_coins'] = favorite_coins
```

The code for the template:

```html
{% if coin in favorite_coins %}
  <a href="#"><i class="fa fa-star"></i></a>
{% else %}
  <a href="#"><i class="fa fa-star-o"></i></a>
{% endif %}
```

##### 4. Write the view

In `urls.py`:

```python
path('favorite/', views.favorite, name='favorite'),
```

In `views.py`:

```python
from django.http import HttpResponse

@login_required
def favorite(request):
    profile = request.user.profile
    coin_id = request.POST['coinId']
    coin = Cryptocurrency.objects.get(id=coin_id)

    if profile.favorite_coins.filter(id=coin_id).exists():
        profile.favorite_coins.remove(coin)
    else:
        profile.favorite_coins.add(coin)

    return HttpResponse("Good!")
```

##### 5. Demonstrate the url template tag
Change `base.html`'s url to favorite from '/favorite/' (hardcoded) to `'favorite_url': "{% url 'favorite' %}"`.
