from django.urls import path
from polls import views

urlpatterns = [
    path("polling-unit/result/", views.PUResultView.as_view(), name="pu-result"),
    path("lga-result/request/", views.LGAResultRequestView.as_view(), name="lga-result-request"),
    path("lga-result/<int:pk>/", views.LGAResultView.as_view(), name="lga-result" ),
    path("polling-unit/add/", views.PollingUnitCreationView.as_view(), name="add-pu"),
    path(
        "polling-unit/<int:pk>/results/add/",
        views.AnnouncedResultCreationView.as_view(),
        name="add-pu-results"
    )
]