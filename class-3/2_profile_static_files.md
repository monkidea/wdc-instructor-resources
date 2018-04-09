Show the avatars, css and js files in static/, config in settings and how it's loaded from templates. Avatars are downloaded from [collection](https://www.behance.net/gallery/47035405/Free-avatars-flat-icons).

### 1 - Static Files

* Show the static directory included in settings.py
* Explain `{% load static%}` the `{% static %}` templatetag.

```html
{% if request.user.is_authenticated %}
  <img src="{% static "img/avatars/256_1.png" %}" alt="" width='30px'>
{% endif %}
```

### 2 - Profile


##### 1. Include a `Profile` model (OneToOne relationship with user + avatr)

```python
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    avatar_picture_name = models.CharField(
        max_length=255, blank=True, default='')
```

##### 2. Create the profile and picture in the admin

Use the shell to walk the relationship User > Profile.

##### 3. Modify the template to include the static block

```html
{% if request.user.is_authenticated %}
  {% if request.user.profile and request.user.profile.avatar_picture_name %}
    {% with 'img/avatars/'|add:request.user.profile.avatar_picture_name as avatar_path %}
       <img src="{% static avatar_path %}" alt="" width='30px'>
    {% endwith %}
  {% else %}
    <img src="{% static "img/avatars/256_1.png" %}" alt="" width='30px'>
  {% endif %}
{% endif %}
```
