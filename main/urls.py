from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
  path("", views.homepage, name="homepage"),
  path("register/", views.RegisterView.as_view(), name='register'),
  path("result/", views.result, name="result"),
  path("edit_input/",views.edit_input, name="edit_input"),
  path("save_result/",views.SaveResult.as_view(), name="save_result"),
  path("your_summarizations/",views.PrevSummarizations.as_view(), name="your_summarizations"),
  path("summarization/delete/<int:pk>/",views.DelSummarization.as_view(), name="delete"),
  path("summarization/detail/<int:pk>/",views.DetailSummarization.as_view(), name="detail"),
]