from django import forms
from burger.models import UserProfile, PointOfInterest, Restaurant, Burgers, BurgerCategories, Comments, BurgerPicture
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

class PlaceForm(forms.ModelForm):
   class Meta:
       model = Restaurant
       fields = ('name', 'desc', 'picture')
       widgets = {
           'name' : forms.TextInput(attrs={'class': 'form-control'}),
           'desc' : forms.TextInput(attrs={'class': 'form-control'}),
           'address' : forms.TextInput(attrs={'class': 'form-control'})
       }
class MapForm(forms.ModelForm):
    class Meta:
        model = PointOfInterest
        fields = ('address', 'city', 'zipcode', 'position')

class BurgerForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(BurgerForm, self).__init__(*args, **kwargs)
        self.fields['location'].empty_label = ""
    class Meta:
        model = Burgers
        exclude = ('worst', 'best')
        # widgets = {'worst': forms.HiddenInput(), 'best': forms.HiddenInput()}

class BurgerCategoryForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = BurgerCategories
        fields = ('name',)
        widgets = {
           # 'name' : forms.TextInput(attrs={'class': 'form-control'}),
           # 'category' : forms.TextInput(attrs={'class': 'form-control'}),
           # 'location' : forms.TextInput(attrs={'class': 'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text', 'rating',)

class BurgerPictureForm(forms.ModelForm):
    class Meta:
        model = BurgerPicture
        fields = ('picture',)
