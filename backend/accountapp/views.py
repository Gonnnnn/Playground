from ast import arg
from django.contrib.auth.models import User
from .models import Article

from django.contrib.auth.forms import UserCreationForm
from .forms import AccountUpdateForm

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorators import *

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

# Create your views here.

has_ownership = [login_required, account_ownership_required]

@login_required
def hello_world(request):
    if request.method == "POST":
        text = request.POST.get('title')
        
        article = Article()
        article.title = text
        article.save()

        # 아래처럼 render로 반환하면 계속 conform from resubmission 경고가 뜬다. 이유 확인해야한다
        # article_list = Article.objects.all()
        # return render(request, 'accountapp/body.html', context={'article_list': article_list})

        return redirect(reverse('accountapp:hello_world'))
    else:
        article_list = Article.objects.all()
        return render(request, 'accountapp/body.html', context={'article_list': article_list})

class AccountCreateView(CreateView):
    # abstractUser을 상속받아서 만들어짐. 우리가 직접 상속받아서 필드를 더 추가해도됨
    model = User
    form_class = UserCreationForm
    # 함수와 클래스가 파이썬에서 불러와지는 방식의 차이 때문에 reverse는 클래스에서 사용할 수 없고 reverse_lazy를 사용 
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/create.html'

class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):
    model = User
    context_object_name = 'target_user'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/update.html'

    # def get(self, *args, **kwargs):
    #     if self.request.user.is_authenticated and self.get_object() == self.request.user.pk:
    #         return super().get(*args, **kwargs)
    #     else:
    #         return HttpResponseForbidden()

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'