from django.urls import path
from django.views.generic.base import TemplateView
from polls import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("polling-unit/result/", views.PUResultView.as_view(), name="pu-result"),
    path("lga-result/request/", views.LGAResultRequestView.as_view(), name="lga-result-request"),
    path("lga-result/<int:pk>/", views.LGAResultView.as_view(), name="lga-result" ),
    path("polling-unit/add/", views.PollingUnitCreationView.as_view(), name="add-pu"),
    path(
        "polling-unit/<int:pk>/results/add/",
        views.AnnouncedResultCreationView.as_view(),
        name="add-pu-results"
    ),
    path(
        "polling-unit/results/add/success",
        TemplateView.as_view(template_name="polls/pollingunit_results_add_success.html"),
        name="pu-result-add-success"
    )
]