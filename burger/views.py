from django.shortcuts import render
from burger.models import PointOfInterest, Burgers, Comments, UserProfile, BurgerPicture
from burger.forms import UserForm, UserProfileForm, PlaceForm, MapForm, BurgerForm, BurgerCategoryForm, CommentForm, BurgerPictureForm
from django.contrib.auth.decorators import login_required
import pygeoip, json
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core import serializers
import re
from django.db.models import Q, Avg

def index(request):
    best = Comments.objects.extra(select={'sum':'rating'}).order_by('-sum')
    comments = Comments.objects.order_by('-date')
    result = {}
    if best:
        result['best'] = best[0]
    if comments:
        result['reviews'] = comments
    return render(request, 'burger/index.html', result)

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'burger/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def registerClosed(request):
    return render(request, 'registration/registration_closed.html')

def map_view(request):
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    data = gi.record_by_addr('109.246.189.234')
    x_address = request.META.get('HTTP_X_FORWARDED_FOR')
    remote_address = request.META.get('REMOTE_ADDR')
    pois = PointOfInterest.objects.all()
    return render(request, 'burger/map_view.html', {'pois': pois, "data": data, "remote": remote_address, "x": x_address})

@login_required
def add_burger(request):
    if request.method == 'POST':
        burger_form = BurgerForm(request.POST)
        burger_picture_form = BurgerPictureForm(request.POST, request.FILES)

        if burger_form.is_valid() and burger_picture_form.is_valid():
            burger = burger_form.save(commit=True)

            burger_pic = burger_picture_form.save(commit=False)
            burger_pic.burger = burger
            burger_pic.slug = burger.slug
            if 'picture' in request.FILES:
                burger_pic.picture = request.FILES['picture']
            burger_pic.save()

            return browse_burger(request)

        else:
            print burger_form.errors
    else:
        burger_form = BurgerForm()
        burger_picture_form = BurgerPictureForm()
        data = serializers.serialize("json", PointOfInterest.objects.all())

    return render(request, 'burger/add_burger.html', {'form':burger_form, 'picForm': burger_picture_form, 'data':data})

@login_required
def add_restaurant(request):
    if request.method == 'POST':
        restaurant_form = PlaceForm(request.POST, request.FILES)
        location_form = MapForm(data=request.POST)

        if restaurant_form.is_valid() and location_form.is_valid():
            restaurant = restaurant_form.save(commit=False)
            if 'picture' in request.FILES:
                restaurant.picture = request.FILES['picture']
            restaurant.save()

            location = location_form.save(commit=False)
            location.name = restaurant.name
            location.restaurant = restaurant
            location.save()

            return index(request)

        else:
            print restaurant_form.errors, location_form.errors
    else:
        restaurant_form = PlaceForm()
        location_form = MapForm()

    return render(request, 'burger/add_place.html', {'restaurant_form':restaurant_form, "location_form": location_form})

@login_required
def add_burger_category(request):
    if request.method == 'POST':

        form = BurgerCategoryForm(request.POST)
        response_data = {}
        
        if form.is_valid():
            form.save(commit=True)
            response_data['result'] = 'created'
            burgerForm = BurgerForm()
            response_data['form'] = render_to_string('burger/burger_form.html', {'form': burgerForm})
        else:
            response_data['result'] = 'form invalid'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def browse_burger(request):
    burgerList = Burgers.objects.all()
    context_dict = {'burgers': burgerList}
    return render(request, 'burger/list_burger.html', context_dict)

def burger_page(request, burger_slug):
    context_dict = {}
    try:
        burger = Burgers.objects.get(slug=burger_slug)
        reviews = Comments.objects.filter(target=burger)
        score = Comments.objects.filter(target=burger).aggregate(Avg('rating'))

        if request.method == 'POST':
            form = CommentForm(request.POST)
            picture_form = BurgerPictureForm(request.POST, request.FILES)

            if form.is_valid() and  picture_form.is_valid():
                if burger:
                    comment = form.save(commit=False)
                    comment.target = burger
                    comment.user = UserProfile.objects.get(user=request.user)
                    comment.save()

                    burger_pic = picture_form.save(commit=False)
                    burger_pic.burger = burger
                    burger_pic.slug = burger.slug
                    if 'picture' in request.FILES:
                        burger_pic.picture = request.FILES['picture']
                    burger_pic.save()

                    reviews = Comments.objects.filter(target=burger)
                    score = Comments.objects.filter(target=burger).aggregate(Avg('rating'))

                    response_data = {}
                    response_data['result'] = "success"
                    response_data['reviews'] = render_to_string('burger/burger_form.html', {'reviews': reviews})
                    response_data['avg_rating'] = score
            else:
                response_data['result'] = 'form invalid'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            form = CommentForm()
            pic_form = BurgerPictureForm()

        context_dict = {'form':form, "picture_form": pic_form, 'burger': burger, 'slug': burger_slug, "reviews": reviews, "avg_rating":score}

    except Burgers.DoesNotExist:
        pass

    return render(request, 'burger/burger.html', context_dict)

def getPictures(request):
    if request.method == 'POST':
        response_data = {}

        pictures = BurgerPicture.objects.all().filter(slug=request.POST.get('slug'))
        urls = []
        for pic in pictures:
            if hasattr(pic.picture, 'url'):
                urls.append(pic.picture.url)
        response_data['urls'] = urls
        response_data['slug'] = request.POST.get('slug')

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

# http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['slug', 'name',])
        
        found_entries = Burgers.objects.filter(entry_query)

        response_data = {'burger': []}
        for burger in found_entries:
            response_data['burger'].append(burger.slug)

    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")
