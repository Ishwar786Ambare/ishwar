from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm

from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

from .forms import EmailPostForm
from .forms import LoginForm, UserRegistrationForm
from django.core.mail import send_mail

from .forms import LoginForm, UserRegistrationForm

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm

from django.contrib import messages

from .models import Profile
@login_required
def dashboard(request):
    return render(request,'account/dashboard.html',{'section': 'dashboard'})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            form = LoginForm()
    form = LoginForm()

    return render(request, 'account/login.html', {'form': form})

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
        # ... send email
    else:
        form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'post': post,
                                                        'form': form})


# def post_share(request, post_id):
#     Retrieve post by id
    # post = get_object_or_404(Post, id=post_id, status='published')
    # sent = False
    # if request.method == 'POST':
    #     Form was submitted
        # form = EmailPostForm(request.POST)
        # if form.is_valid():
        #       Form fields passed validation
              # cd = form.cleaned_data
              # post_url = request.build_absolute_uri(post.get_absolute_url())
              # subject = f"{cd['name']} recommends you read " \
              #           f"{post.title}"
              # message = f"Read {post.title} at {post_url}\n\n" \
              #           f"{cd['name']}\'s comments: {cd['comments']}"
              # send_mail(subject, message, 'admin@myblog.com',
              #           [cd['to']])sent = True
              # else:
              # form = EmailPostForm()
              # return render(request, 'blog/post/share.html', {'post': post,
              #                                                 'form': form,
              #                                                 'sent': sent})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,'account/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html',{'user_form': user_form,'profile_form': profile_form})