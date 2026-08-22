from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from pathlib import Path 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import INTERNAL_RESET_SESSION_TOKEN, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib import messages # type: ignore
from .forms import CreateUserForm
from rest_framework.authtoken.models import Token # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from . filters import DetectionFilter
from . models import UploadAlert

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is None and username and '@' in username:
                matched = User.objects.filter(email__iexact=username).first()
                if matched:
                    user = authenticate(request, username=matched.username, password=password)

            if user is not None:
                login(request, user) 
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)
            
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was successfully created for ' + user)
                return redirect('login')
        context = {'form':form}
        return render(request, 'register.html', context)
    
@login_required(login_url='login')
def home(request): 
    token = Token.objects.get(user=request.user)
    uploadAlert = UploadAlert.objects.filter(user_ID= token)
    myFilter = DetectionFilter(request.GET, queryset=uploadAlert)
    uploadAlert = myFilter.qs
    context = {'myFilter': myFilter, 'uploadAlert':uploadAlert}
    return render(request, 'dashboard.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "password_reset_form.html"
    success_url = reverse_lazy('home')
    post_reset_login = True
    post_reset_login_backend = 'django.contrib.auth.backends.ModelBackend'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        # Validate the token from the URL on GET and POST. Django's default
        # flow moves the token into the session and redirects to /set-password/,
        # which email clients can prefetch and which leaves the real browser
        # without a valid session — the form then submits but never saves.
        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])
        token = kwargs.get('token')

        if self.user is not None and token:
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if session_token and self.token_generator.check_token(self.user, session_token):
                    self.validlink = True
            elif self.token_generator.check_token(self.user, token):
                self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                self.validlink = True

        if self.validlink:
            return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        user = form.save()
        self.request.session.pop(INTERNAL_RESET_SESSION_TOKEN, None)
        login(self.request, user, self.post_reset_login_backend)
        messages.success(self.request, 'Password reset successful.')
        return super(PasswordResetConfirmView, self).form_valid(form)

def passwordResetComplete(request):
    messages.success(request, 'Password reset successful. Please log in.')
    return redirect('login')

def alert(request, pk):
    uploadAlert = UploadAlert.objects.filter(image = str(pk) + ".jpg")
    myFilter = DetectionFilter(request.GET, queryset=uploadAlert)
    uploadAlert = myFilter.qs
    context = {'myFilter':myFilter, 'uploadAlert':uploadAlert}

    return render(request, 'alert.html', context)

def alert_image(request, pk):
    alert = get_object_or_404(UploadAlert, image=str(pk) + '.jpg')
    image_path = Path(alert.image.path)
    if not image_path.exists():
        raise Http404('Image not found')
    return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
    

