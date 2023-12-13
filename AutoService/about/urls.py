from django.urls import path
from django.views import generic
from . import views

app_name = "about"
urlpatterns = [
    path("policy", generic.TemplateView.as_view(template_name="about/policy.html"), name="policy"),
    path("vacancies", views.VacanciesView.as_view(template_name="about/vacancies.html"), name="vacancies"),
    path("stats", views.StatsView.as_view(template_name='about/stats.html'), name="stats"),
    path("faq", views.QuestionsView.as_view(template_name="about/faq.html"), name="faq"),
    path("articles", views.ArticlesView.as_view(template_name="about/articles.html"), name="articles"),
    path("article/<int:pk>", views.ArticleView.as_view(template_name="about/article.html"), name="article"),
    path("about", generic.TemplateView.as_view(template_name="about/about.html"), name="about"),
    path("home", views.HomeView.as_view(template_name="about/home.html"), name="home"),
]

