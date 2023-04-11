from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


@login_required
def profile_view(request):
    if request.method == 'GET':
        user_profile = User.objects.get(pk=request.user.id)

        return render(request, 'profile_detail.html', {'user_profile': user_profile})
