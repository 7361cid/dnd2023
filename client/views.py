from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.edit import FormView

from .models import CustomClient, Product
from .forms import RegisterForm, UserUpdateForm


class Signup(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'registration\\signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        print(f"DEBUG post Signup {form}")
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = CustomClient.objects.get(username=username)
            if 'profile_avatar' in request.FILES.keys():
                user.profile_avatar = request.FILES['profile_avatar']
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        return render(request, 'registration\\signup.html', {'form': form})


class Login(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        csrf_token = get_token(request)
        return render(None, 'registration\\login.html', {'csrf_token': csrf_token})

    def post(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        print(f"DEBUG post {csrf_token}")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
        return render(None, 'registration\\login.html', {'csrf_token': csrf_token})


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')


class UserPage(FormView):
    template_name = 'user_profile.html'
    form_class = UserUpdateForm
    success_url = '/'

    def get(self, request, pk, *args, **kwargs):
        page_user = get_object_or_404(CustomClient, id=pk)
        form = UserUpdateForm()
        context = {'form': form, 'page_user': page_user}
        if request.user.is_authenticated:
            context['user_avatar'] = request.user.profile_avatar

        context['page_user_avatar'] = page_user.profile_avatar
        print(f"UserPage LOG {context}")
        user_products_dict = {}
        user_products = Product.objects.filter(user_pk=page_user.pk)
        # for user_product in user_products:
        #     if user_product.product_pk in user_products_dict:
        #         user_products_dict[user_product.product_pk]["quantity"] += user_product.count
        #     else:
        #         user_products_dict[user_product.product_pk] = {
        #             "product": Product.objects.get(pk=user_product.product_pk),
        #             "quantity": user_product.count}
        for user_product in user_products:
            print(f"UserPage LOG {user_product}")
            user_products_dict[user_product.pk] = {"product": user_product, "quantity": 1}
        print(f"UserPage LOG user_products_dict {user_products_dict}")
        context["user_products_dict"] = user_products_dict
        return render(request, 'user_profile.html', context)

    def form_valid(self, form):
        page_user = self.request.user
        if form.data['email']:
            page_user.email = form.cleaned_data['email']
            page_user.save()
        if "profile_avatar" in self.request.FILES.keys():
            page_user.profile_avatar = self.request.FILES['profile_avatar']
            page_user.save()

        context = {'form': form, 'page_user': page_user}
        if self.request.user.is_authenticated:
            context['user_avatar'] = page_user.profile_avatar
        context['page_user_avatar'] = page_user.profile_avatar
        return render(self.request, 'user_profile.html', context)


def main_page(request):
    context = {}
    if request.user.is_authenticated:
        context['user_avatar'] = request.user.profile_avatar
    print(f"UserPage LOG {context}")
    return render(request, 'home.html', context)
