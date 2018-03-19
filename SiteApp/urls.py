from django.urls import path
from .views import *

urlpatterns = [
    path('', QuestionList.as_view()),
    path('login/', LogIn.as_view()),
    path('signup/', SignUp.as_view()),
    path('logout/', logout_view),
    path('settings/', Settings.as_view()),
    path('ask/', QuestionCreate.as_view()),
    path('question/id<int:pk>', Question.as_view()),
]
