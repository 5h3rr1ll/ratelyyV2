from django.conf.urls  import include, url
from . import views

app_name = "database"

urlpatterns = [
    #Used as both the main page url, and for the search-form submission.
    #If the GET object exists, then the search-form is being submitted.
    #Otherwise, it's a normal page request.
    url(r"^$", views.Database.as_view(), name="database"), #hieß vorher name="color_list"
    url(r"^search/$", views.submit_search_from_ajax, name="search"), # hieß vorher: name="color_list"
    url(r"^details/(?P<brand_id>\d+)/$", views.BrandDetails, name="BrandDetails"),
    url(r"^konzerne/(?P<buchstabe>\w+)/$", views.KonzernListe, name="kListe"),
    url(r"^konzerne/$", views.Konzerne, name="konzerne"),
    url(r"^unternehmen/$", views.Unternehmen, name="unternehmen"),
    url(r"^unternehmen/(?P<buchstabe>\w+)/$", views.UnternehmenListe, name="uListe"),
    url(r"^marken/$", views.Marken, name="marken"),
    url(r"^marken/(?P<buchstabe>\w+)/$", views.MarkenListe, name="mListe"),
]
