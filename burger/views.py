from django.shortcuts import render
from burger.models import Category, Page, PointOfInterest, Restaurant, Burgers
from burger.forms import CategoryForm, PageForm, UserForm, UserProfileForm, PlaceForm, MapForm, BurgerForm
from django.contrib.auth.decorators import login_required
import pygeoip

def index(request):
    # return HttpResponse("Burger says hey hunger game!")
    best = Burgers.objects.all().filter(best=True)
    worst = Burgers.objects.all().filter(worst=True)
    context_dict = {'boldmessage': "I am bold font from the context", 'best': best[0], 'worst': worst[0]}
    return render(request, 'burger/index.html', context_dict)

@login_required
def categoryList(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    return render(request, 'burger/categoryList.html', context_dict)

def category(request, category_name_slug):
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
        context_dict['slug'] = category_name_slug
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'burger/category.html', context_dict)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return categoryList(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'burger/add_category.html', {'form': form})

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat, 'slug': category_name_slug}

    return render(request, 'burger/add_page.html', context_dict)

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

def map(request):
    if request.method == 'POST':
        form = MapForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = MapForm()

    return render(request, 'burger/map.html', {'form': form})

def map_view(request):
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    data = gi.record_by_addr('109.246.189.234')
    # client_address = request.META.get('HTTP_X_FORWARDED_FOR')
    client_address = request.META.get('REMOTE_ADDR')
    pois = PointOfInterest.objects.all()
    return render(request, 'burger/map_view.html', {'pois': pois, "data": data, "ip": client_address})


def add_burger(request):
    if request.method == 'POST':
        burger_form = BurgerForm(request.POST, request.FILES)


        if burger_form.is_valid():
            burger= burger_form.save(commit=False)
            if 'picture' in request.FILES:
                burger.picture = request.FILES['picture']
            burger.save()

            return index(request)

        else:
            print burger_form.errors
    else:
        burger_form = BurgerForm()


    return render(request, 'burger/add_burger.html', {'form':burger_form})


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
