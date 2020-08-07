from taggit.models import Tag
from django.views import View
from signin.models import Profile, Hiree
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from signin.forms import CustomUserChangeForm, ProfileForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404


def home(request):
    categories = Profile._meta.get_field('category').choices
    popular_tags = Profile.skills.most_common()[:10]

    user_excluded_queryset = Profile.objects.exclude(user__id=request.user.id)
    recently_added = user_excluded_queryset.filter(
        user__is_superuser=False,
        available_for_hire=True
    ).order_by('-joined_at')[:8]

    return render(request, 'pages/home.html', {
        'categories': categories,
        'popular_tags': popular_tags,
        'recently_added': recently_added,
    })


class DashboardView(LoginRequiredMixin, View):
    template_name = 'pages/dashboard.html'

    def get(self, request, *args, **kwargs):
        incomings = []
        if Hiree.objects.filter(hirer_id=request.user.id).exists():
            incomings = Hiree.objects.get(hirer=request.user).hirees.all()

        outgoings = Hiree.objects.filter(hirees=request.user)

        print(outgoings)

        return render(request, self.template_name, {
            'incomings': incomings,
            'outgoings': outgoings,
        })


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
            request.POST, instance=request.user.profile
        )

        if user_change_form.is_valid() and user_profile_form.is_valid():
            update_user_changes = user_change_form.save()

            updated_user_profile = user_profile_form.save(commit=False)
            updated_user_profile.user = request.user
            updated_user_profile.save()

            user_profile_form.save_m2m()
            return redirect('dashboard')


        # print(user_profile_form.is_valid())

        return render(request, self.template_name, {
            'user_form': user_change_form,
            'profile_form': user_profile_form
        })


class SearchResultsView(View):
    template_name = 'listings/search_results.html'

    def get(self, request, *args, **kwargs):
        # query = request.GET.get('q')
        #
        # search_item = get_object_or_404(Tag, slug=query)
        # queryset = Profile.objects.filter(available_for_hire=True,
        #                                   skills=search_item)

        search_items = request.GET.get('q').lower().replace(' ','').split(',')
        price1 = request.GET.get('min')
        price2 = request.GET.get('max')
        if not price1:
            price1=0
        if not price2:
            price2=1000

        user_excluded_queryset = Profile.objects.exclude(user__id=request.user.id)
        queryset = user_excluded_queryset.filter(
            available_for_hire=True,
            skills__name__in=search_items,
            price__range=(price1, price2)
        ).order_by('user__date_joined').distinct()

        paginator = Paginator(queryset, 3)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)

        return render(request, self.template_name, {
            'page_obj': page_obj
        })


class TagListView(View):
    queryset = Tag.objects.all()
    template_name = 'listings/tag_list.html'

    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.queryset, 12)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)

        return render(request, self.template_name, {
            'page_obj': page_obj
        })


class TagDetailsView(View):
    template_name = 'listings/tag_details.html'

    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        user_excluded_queryset = Profile.objects.exclude(user__id=request.user.id)
        queryset = user_excluded_queryset.filter(available_for_hire=True,
                                          skills=tag)

        paginator = Paginator(queryset, 10)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)

        return render(request, self.template_name, {
            'page_obj': page_obj
        })

class PublicProfileView(View):
    template_name = 'pages/public_profile.html'
    comment_form_class = CommentForm

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, id=pk)
        comments = user.profile.comment_set.all()
        form = self.comment_form_class()
        profile = user.profile

        is_favourite = False
        involved = False
        already_commented = False
        if request.user.is_authenticated:
            if request.user.profile.favourite.filter(id=user.id).exists():
                is_favourite = True

            incomings = User.objects.none()
            if Hiree.objects.filter(hirer_id=request.user.id).exists():
                incomings = Hiree.objects.get(hirer=request.user).hirees.all()

            outgoings = Hiree.objects.filter(hirees=request.user)

            involved = any([
                incomings.filter(id=pk).exists(),
                outgoings.filter(hirer_id=pk).exists()
            ])

            if profile.comment_set.filter(user=request.user).exists():
                already_commented = True

        # print(is_favourite)
        return render(request, self.template_name, {
            'profile': user.profile,
            'involved': involved,
            'form': form,
            'comments': comments,
            'is_favourite': is_favourite,
            'already_commented': already_commented,
        })


class UserActionView(LoginRequiredMixin,View):
    def get(self, request, pk, action):
        return redirect('public_profile', pk=pk)

    def post(self, request, pk, action):
        new_hire = get_object_or_404(User, id=pk)
        if action == 'hire':
            Hiree.hire(request.user, new_hire)
        else:
            Hiree.free(request.user, new_hire)

        return redirect('dashboard')


class CommentView(LoginRequiredMixin, View):
    comment_form_class = CommentForm

    def post(self, request, pk):
        owner = get_object_or_404(User, id=pk)
        profile = owner.profile

        form = self.comment_form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.profile = profile

            # print(new_comment)
            new_comment.save()

        return redirect('public_profile', pk=pk)

def add_favourite(request, pk):
        fav = get_object_or_404(User, id=pk)

        if request.user.profile.favourite.filter(id=fav.id).exists():
            # print('removed')
            request.user.profile.favourite.remove(fav)
        else:
            # print('saved')
            request.user.profile.favourite.add(fav)
        return redirect('public_profile', pk=pk)

def list_favourites(request):
        user = request.user
        favs = user.profile.favourite.all()
        # print(favs)
        context = {
            'favs': favs,
        }
        return render(request, 'pages/profile_favourite_list.html', context)


class CategoryListView(View):
    template_name = 'listings/category_list.html'

    def get(self, request):
        categories = Profile._meta.get_field('category').choices

        return render(request, self.template_name, {
            'categories': categories
        })

class CategoryDetailsView(View):
    template_name = 'listings/category_details.html'

    def get(self, request, cat):
        queryset = Profile.objects.exclude(user__id=request.user.id)
        queryset = queryset.filter(
            category=cat,
            available_for_hire=True
        )

        paginator = Paginator(queryset, 1)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)

        return render(request, self.template_name, {
            'page_obj': page_obj
        })
