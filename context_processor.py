from accounts.models import Profile
from product.models import Category


def general_context(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        parents = Category.objects.filter(parent=None)
        context = {
            'profile' : profile,
            'parents' : parents,
        }
    else:

        parents = Category.objects.filter(parent=None)
        context = { 'parents': parents, }

    return context