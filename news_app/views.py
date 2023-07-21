from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,  get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView

from .forms import ContactForm
from .models import News, Category

def news_list(request):
    news_list = News.objects.filter(status=News.Status.Published)
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        "news": news
    }

    return render(request, 'news/news_detail.html', context)
#pastdagi kod hamePageView uchun sababi bu kod funksiyani ichida iwlamadi
x = News.objects.filter(status=News.Status.Published)
def homePageView(request):

    categories = Category.objects.all()
    news_list1 = News.objects.filter(status=News.Status.Published).order_by('-publish_time')[8:13]
    news_list = News.objects.filter(status=News.Status.Published).order_by('-publish_time')[:5]
    news_listt = News.objects.filter(status=News.Status.Published).order_by('-publish_time')
    #local_one = x.filter(category__name="Mahalliy")[:1]
    sport_news = x.filter(category__name="Sport")[:5]
    tecnology_news = x.filter(category__name="Texnologiya")[:5]
    yevro_news = x.filter(category__name="Xorij")[:5]
    local_news = x.filter(category__name="Mahalliy")[:5]

    context = {
        'news_listt': news_listt,
        'news_list': news_list,
        'categories': categories,
        'local_news': local_news,
       # 'local_one': local_one,
        'news_list1': news_list1,
        'sport_news': sport_news,
        'tecnology_news': tecnology_news,
        'yevro_news': yevro_news

    }

    return render(request, 'news/home.html', context)

"""class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.model.objects.all()
        context['news_list'] = News.objects.filter(status=News.Status.Published).order_by('-publish_time')[:10]
        context['local_one'] = x.filter(category__name="Mahalliy")[:1]
        context['local_news'] = x.filter(category__name="Mahalliy")[1:5]
        return context"""



'''def contactView(request):
    print(request.POST)
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponse("<h2> biz bilan boglanganingiz uchun rahmat")
    context = {
        "form": form
    }

    return render(request, 'news/contact.html', context)'''

def About(request):
    context = {

    }
    return render(request, 'news/base.html', context)

def eror(request):
    context = {

    }
    return render(request, 'news/404.html', context)

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm
        context = {
            "form": form
        }

        return render(request, 'news/contact.html', context)

    def post(self,request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2> biz bilan boglanganingiz uchun rahmat")
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)

class LocalPageView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news =  x.filter(category__name="Mahalliy")
        return news

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news =  x.filter(category__name="Xorij")
        return news

class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologik_yangiliklar'

    def get_queryset(self):
        news =  x.filter(category__name="Texnologiya")
        return news

class SportPageView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news =  x.filter(category__name="Sport")
        return news


class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status', )
    template_name = "crud/news_edit.html"

class NewsDeleteView(DeleteView):
    model = News
    template_name = "crud/news_delete.html"
    success_url = reverse_lazy('home_page')

class NewsCreateView(CreateView):
    model = News
    template_name = "crud/news_create.html"
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')

class SearchResultList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'
    def get_queryset(self):
        query = self.request.GET.get('q')
        return  News.objects.filter(
            Q(title__icontains=query ) | Q( body__icontains=query)
        )