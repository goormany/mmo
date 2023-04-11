from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Exists
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.template import RequestContext
from .filters import RequestsFilter
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import Author, Category, Post, ResponsePost
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from .forms import CreatePostForm, CreateRespondForm


class PostListView(ListView):
    model = Post
    template_name = 'post_lists.html'
    context_object_name = 'posts'
    ordering = '-date_created'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_post',)
    raise_exception = True
    template_name = 'post_create.html'
    form_class = CreatePostForm
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author_post = Author.objects.get(author_user=self.request.user.id)
        return super().form_valid(form)


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_post',)
    template_name = 'post_create.html'
    model = Post
    form_class = CreatePostForm
    raise_exception = True

    def get(self, request, **kwargs):
        if self.get_object().author_post == Author.objects.get(author_user=self.request.user):
            return UpdateView.get(self, request, **kwargs)
        else:
            return render(request, '403.html')


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get(self, request, **kwargs):
        if self.get_object().author_post == Author.objects.get(author_user=self.request.user):
            return DeleteView.get(self, request, **kwargs)
        else:
            return render(request, '403.html')


@login_required
@csrf_protect
def responds(request, **kwargs):
    if request.method == 'POST':
        post_id = Post.objects.get(pk=kwargs['pk'])
        form = CreateRespondForm(request.POST)

        if form.is_valid():
            user_sender_id = User.objects.get(pk=request.user.id)
            text_ = form.cleaned_data['text']
            if ResponsePost.objects.filter(user_sender=user_sender_id, post=post_id).exists():
                messages.info(request, messages.WARNING, 'Вы уже отправляли отклик на этото объявление')
            else:
                ResponsePost.objects.create(post=post_id, user_sender=user_sender_id, text=text_)
            return HttpResponseRedirect('/')

    else:
        form = CreateRespondForm()

    return render(request, 'respond_create.html', {'form': form})


class ResponseListView(LoginRequiredMixin, ListView):
    context_object_name = 'responses'
    model = ResponsePost
    template_name = 'respond_list.html'
    ordering = '-date_created'


class ResponceListView(LoginRequiredMixin, ListView):
    model = ResponsePost
    template_name = 'respond_list.html'
    context_object_name = 'rr'

    def post(self, request, *args, **kwargs):
        action = None
        action = request.POST.get('action')
        r = ResponsePost.objects.get(id=ResponsePost.objects.get(id=request.POST.get('category_id')).id)
        if action == 'acceptR':
            r.status = 'A'
            r.save()
        elif action == 'deniedR':
            r.status = 'D'
            r.save()
        return redirect(to='/responses/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        status = self.request.GET.get('status')
        if status == 'D':
            context['rrr'] = ResponsePost.objects.filter(post__author_post=self.request.user.id, status=status)
        elif status == 'A':
            context['rrr'] = ResponsePost.objects.filter(post__author_post=self.request.user.id, status=status)
        elif status == 'N':
            context['rrr'] = ResponsePost.objects.filter(post__author_post=self.request.user.id, status=status)
        else:
            context['rrr'] = ResponsePost.objects.filter(post__author_post=self.request.user.id)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RequestsFilter(self.request.GET, queryset)
        return self.filterset.qs


