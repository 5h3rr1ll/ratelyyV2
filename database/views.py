from django.shortcuts     import render_to_response
from django.views.generic import ListView
from database.models   import Concern, Company, Brand, Product

MIN_SEARCH_CHARS = 1
"""
The minimum number of characters required in a search. If there are less,
the form submission is ignored. This value is used by the below view and
the template.
"""
class Database(ListView):
    """
    Displays all Concerns, Companies, Brands and in the future also Products, in
    a table with only one column.
    """
    model = Brand
    context_object_name = "colors"
    template_name = "database/index.html"

    def dispatch(self, request, *args, **kwargs):
        return super(Database, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        This returns the all colors, for display in the main table.

        The search result query set, if any, is passed as context.
        """
        return  super(Database, self).get_queryset()

    def get_context_data(self, **kwargs):
        #Get the current context.
        context = super(Database, self).get_context_data(**kwargs)

        context["MIN_SEARCH_CHARS"] = MIN_SEARCH_CHARS

        return  context

def submit_search_from_ajax(request):
    """
    Processes a search request, ignoring any where less than two
    characters are provided. The search text is both trimmed and
    lower-cased.

    See <link to MIN_SEARCH_CHARS>
    """

    colors = []  #Assume no results.

    global  MIN_SEARCH_CHARS

    search_text = ""   #Assume no search
    if(request.method == "GET"):
        search_text = request.GET.get("search", "").strip().lower()
        if(len(search_text) < MIN_SEARCH_CHARS):
            """
            Ignore the search. This is also validated by
            JavaScript, and should never reach here, but remains
            as prevention.
            """
            search_text = ""

    #Assume no results.
    #Use an empty list instead of None. In the template, use
    #   {% if color_search_results.count > 0 %}
    search_results = []

    if(search_text != ""):
        # Ergbenis für Treffer in Tabelle Brand
        brands_query = Brand.objects.filter(name__contains=search_text)
        #Ergebenis für Treffer in Tabelle Konzerne
        concerns_query = Concern.objects.filter(name__contains=search_text)
        #Ergebenis für Treffer in Tabelle Unternehmen
        companies_query = Company.objects.filter(name__contains=search_text)

    #print('search_text="' + search_text + '", results=' + str(search_results))

    # im Jinja wird der Key des Dictionary's eingetragen, sodass der Value dann
    # via rendering in dem HTML wiedergegeben werden kann.

    context = {
        "search_text": search_text,
        "MIN_SEARCH_CHARS": MIN_SEARCH_CHARS,
        "search_results": brands_query,
        "concerns_query": concerns_query,
        "companies_query": companies_query,
    };

    return render_to_response("database/search_results_html_snippet.txt",
                               context)

def BrandDetails(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    brand_name = brand.name
    brand_pic = brand.img
    '''
    da bei den Marken noch keine Unternehmen einegtragen sind, wir hier noch
    mit objects.filter gearbeietet, damit kein Fehler geworfen wird.
    '''
    brand_company = Company.objects.filter(id=brand.company)
    brand_concern = Concern.objects.get(id=brand.concern.pk).name
    brand_fair = brand.fair
    brand_eco = brand.eco
    brand_url = brand.url
    brand_concern_url = Concern.objects.get(id=brand.concern.pk).url

    context = {
        "brand_id": brand.id,
        "brand_name": brand.name,
        "brand_pic": brand.img,
        "brand_concern": brand_concern,
        "brand_fair": brand_fair,
        "brand_eco": brand_eco,
        "brand_url": brand_url,
        "brand_concern_url": brand_concern_url,
    }

    return render_to_response("database/details.html", context)

def toggle_color_like(request, color_id):
    """Toggle "like" for a single color, then refresh the color-list page."""
    color = None
    try:
        #There's only one object with this id, but this returns a list
        #of length one. Get the first (index 0)
        color = Brand.objects.filter(id=color_id)[0]
    except Brand.DoesNotExist as e:
        raise  ValueError("Unknown color.id=" + str(color_id) + ". Original error: " + str(e))

    #print("pre-toggle:  color_id=" + str(color_id) + ", color.is_favorited=" + str(color.is_favorited) + "")

    color.is_favorited = not color.is_favorited
    color.save()  #Commit the change to the database

    #print("post-toggle: color_id=" + str(color_id) + ", color.is_favorited=" + str(color.is_favorited) + "")

    #Render the just-clicked-on like-button.
    return  render_to_response("database/color_like_link__html_snippet.txt",
                           {"color": color})
