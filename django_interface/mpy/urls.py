from django.conf.urls import url

from . import views

# app_name makes namespace, just as in c++ you would do namespace mpy {...}
app_name = 'mpy'
urlpatterns = [
    # 'r' before string '...' is because reg-exp contains a lot of back slashes
    # etc. think of it something like "raw"
    url(r'^$', views.index, name='index'),

    # RegExp cheat sheet, remember this module gets yoursite.com/THIS_STRING
    # r                 - not regexp, but Python to indicate "raw",
    #                     helpful since regexp contains a lot of \ etc.
    # ^                 - start of string
    # $                 - end of string
    # +                 - one or more, e.g. above: question_id can be 33
    # (?<name>regex)    - captures text matched by regexp into group "name"
    # (?P<name>regex)   - captures text matched by regexp into group "name"
]
