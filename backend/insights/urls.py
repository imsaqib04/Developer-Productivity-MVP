from django.urls import path
from .views import (
    health_check,
    developers_list,
    managers_list,
    months_list,
    ic_insight_view,
    manager_summary_view,
)

urlpatterns = [
    path("health/", health_check),
    path("developers/", developers_list),
    path("managers/", managers_list),
    path("months/", months_list),
    path("insights/ic/", ic_insight_view),
    path("insights/manager/", manager_summary_view),
]
