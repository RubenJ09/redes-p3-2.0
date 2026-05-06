from django.urls import path

from rules.views import RuleCreateView, RuleDeleteView, RuleListView, RuleUpdateView

app_name = "rules"

urlpatterns = [
    path("", RuleListView.as_view(), name="list"),
    path("create/", RuleCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", RuleUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", RuleDeleteView.as_view(), name="delete"),
]