from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth import logout, authenticate, login
from .forms import *
from re import split as resplit


class QuestionCreate(CreateView):
    form_class = QuestionFrom
    template_name = "question_create.html"
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        tag_titles = resplit(r'[, ]', form.cleaned_data['tags'].lower())
        new_quest = form.save(commit=False)
        new_quest.author_id = request.user.id
        new_quest.save()
        for title in tag_titles:
            try:
                tag = Tag.objects.get(title=title)
            except ObjectDoesNotExist:
                tag = Tag.objects.create(title=title)
            new_quest.tags.add(tag)
        return redirect('/question/id' + str(new_quest.pk))


class QuestionList(ListView):
    model = Quest
    template_name = 'question_list.html'


class Question(DetailView):
    model = Quest
    form_class = AnswerForm
    template_name = 'question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_form'] = self.form_class
        context['answers'] = Answer.objects.filter(question_id=self.kwargs['pk'])
        obj = context['quest']
        context['points'] = obj.likes.count() - obj.dislikes.count()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        new_answer = form.save(commit=False)
        new_answer.author_id = request.user.pk
        new_answer.question_id = kwargs['pk']
        new_answer.save()
        return super(Question, self).get(request, *args, **kwargs)


class LogIn(FormView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class SignUp(CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = '/login/'


class Settings(UpdateView):
    model = User
    fields = ['email', 'nickname', 'avatar']
    template_name = 'user_update.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        self.kwargs[self.pk_url_kwarg] = request.user.pk
        return super(Settings, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.kwargs[self.pk_url_kwarg] = request.user.pk
        return super(Settings, self).post(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect('/')
