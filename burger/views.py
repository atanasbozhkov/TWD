from django.shortcuts import render
from burger.models import PointOfInterest, Burgers, Comments, UserProfile
from burger.forms import UserForm, UserProfileForm, PlaceForm, MapForm, BurgerForm, BurgerCategoryForm, CommentForm
from django.contrib.auth.decorators import login_required
import pygeoip, json
from django.http import HttpResponse
from django.template.loader import render_to_string

def index(request):
    # return HttpResponse("Burger says hey hunger game!")
    best = Burgers.objects.all().filter(best=True)
    worst = Burgers.objects.all().filter(worst=True)
    if(best):
        if(worst):
             context_dict = {'boldmessage': "I am bold font from the context", 'best': best[0], 'worst': worst[0]}
    else:
         context_dict = {'boldmessage': "I am bold font from the context"}
    return render(request, 'burger/index.html', context_dict)

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
    # client_address = request.META.get('HTTP_X_FORWARDED_FOR')
    client_address = request.META.get('REMOTE_ADDR')
    pois = PointOfInterest.objects.all()
    return render(request, 'burger/map_view.html', {'pois': pois, "data": data, "ip": client_address})

@login_required
def add_burger(request):
    if request.method == 'POST':
        burger_form = BurgerForm(request.POST, request.FILES)


        if burger_form.is_valid():
            burger= burger_form.save(commit=False)
            if 'picture' in request.FILES:
                burger.picture = request.FILES['picture']
            burger.save()

            return browse_burger(request)

        else:
            print burger_form.errors
    else:
        burger_form = BurgerForm()


    return render(request, 'burger/add_burger.html', {'form':burger_form})

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

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                if burger:
                    comment = form.save(commit=False)
                    comment.target = burger
                    # comment.user = request.user
                    comment.user = UserProfile.objects.get(user=request.user)
                    comment.save()

                    # profile = UserProfile.objects.get(user=request.user)
                    response_data = {}
                    response_data['result'] = "success"
                    response_data['reviews'] = render_to_string('burger/burger_form.html', {'reviews': Comments.objects.filter(target=burger)})
            else:
                response_data['result'] = 'form invalid'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            form = CommentForm()

        context_dict = {'form':form, 'burger': burger, 'slug': burger_slug, "reviews": reviews}

    except Burgers.DoesNotExist:
        pass

    return render(request, 'burger/burger.html', context_dict)
