from taggit.models import Tag
from django.views import View
from signin.models import Profile
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from signin.forms import CustomUserChangeForm, ProfileForm
from django.shortcuts import render, redirect, get_object_or_404


def home(request):
    return render(request, 'pages/home.html')


class DashboardView(LoginRequiredMixin, View):
    template_name = 'pages/dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    user_change_form_class = CustomUserChangeForm
    user_profile_form_class = ProfileForm
    template_name = 'pages/profile.html'

    def get(self, request, *args, **kwargs):
        user_change_form = self.user_change_form_class(instance=request.user)
        user_profile_form = self.user_profile_form_class(
            instance=request.user.profile
        )

        return render(request, self.template_name, {
            'user_form': user_change_form,
            'profile_form': user_profile_form
        })

    def post(self, request, *args, **kwargs):
        user_change_form = self.user_change_form_class(request.POST,
                                                       instance=request.user)
        user_profile_form = self.user_profile_form_class(
            request.POST, instance=request.user.profile)

        if user_change_form.is_valid() and user_profile_form.is_valid():
            update_user_changes = user_change_form.save()

            updated_user_profile = user_profile_form.save(commit=False)
            updated_user_profile.user = request.user
            updated_user_profile.save()

            user_profile_form.save_m2m()
            return redirect('dashboard')

        return render(request, self.template_name, {
            'user_form': user_change_form,
            'profile_form': user_profile_form
        })


class SearchResultsView(View):
    template_name = 'listings/search_results.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')

        search_item = get_object_or_404(Tag, slug=query)
        results = Profile.objects.filter(available_for_hire=True,
                                         skills=search_item)

        return render(request, self.template_name, {'results': results})


class CategoryListView(View):
    queryset = Tag.objects.all()
    template_name = 'listings/category_list.html'

    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.queryset, 2)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)

        return render(request, self.template_name, {
            'page_obj': page_obj
        })


class CategoryDetailsView(View):
    template_name = 'listings/category_details.html'

    def get(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Tag, slug=slug)
        queryset = Profile.objects.filter(available_for_hire=True,
                                          skills=category)

        paginator = Paginator(queryset, 2)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)

        return render(request, self.template_name, {
            'page_obj': page_obj
        })



