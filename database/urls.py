from django.conf.urls  import include, url
# from views import toggle_color_like, ColorList
from . import views

urlpatterns = [
    #Used as both the main page url, and for the search-form submission.
    #If the GET object exists, then the search-form is being submitted.
    #Otherwise, it's a normal page request.
    url(r"^$", views.Database.as_view(), name="color_list"),
    url(r"^like_color_(?P<color_id>\d+)/$", views.toggle_color_like, name="toggle_color_like"),
    url(r"^search/$", views.submit_color_search_from_ajax, name="color_list"),
]
