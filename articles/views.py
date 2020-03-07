from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView,UpdateView,DeleteView,CreateView
from .models import Article
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy


class ArticleListView(LoginRequiredMixin,ListView):
    model = Article
    template_name = 'articles_list.html'
    login_url = 'login'

class ArticleDetailView(LoginRequiredMixin,DetailView):
    model = Article
    template_name = 'articles_detail.html'
    login_url = 'login'

class ArticleUpdateView(LoginRequiredMixin,UpdateView):
    model = Article
    fields = ('title','body',)
    template_name = 'articles_edit.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author!=self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ArticleDeleteView(LoginRequiredMixin,DeleteView):
    model = Article
    template_name = 'articles_delete.html'
    login_url = 'login'
    success_url  = reverse_lazy('article_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author!=self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = Article
    template_name = 'articles_new.html'
    fields = ('title','body',)
    login_url = 'login'
    success_url  = reverse_lazy('article_list')

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


