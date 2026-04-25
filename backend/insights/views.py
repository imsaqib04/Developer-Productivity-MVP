from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    DeveloperSerializer,
    ManagerSerializer,
    IcInsightSerializer,
    ManagerSummarySerializer,
)
from .services import (
    get_developers,
    get_managers,
    get_months,
    get_ic_insight,
    get_manager_summary,
)


@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"})


@api_view(["GET"])
def developers_list(request):
    developers = get_developers()
    return Response(DeveloperSerializer(developers, many=True).data)


@api_view(["GET"])
def managers_list(request):
    managers = get_managers()
    return Response(ManagerSerializer(managers, many=True).data)


@api_view(["GET"])
def months_list(request):
    return Response(get_months())


@api_view(["GET"])
def ic_insight_view(request):
    developer_id = request.GET.get("developer_id")
    month = request.GET.get("month")

    if not developer_id or not month:
        return Response(
            {"detail": "developer_id and month are required query params"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    insight = get_ic_insight(developer_id, month)
    if not insight:
        return Response({"detail": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(IcInsightSerializer(insight).data)


@api_view(["GET"])
def manager_summary_view(request):
    manager_id = request.GET.get("manager_id")
    month = request.GET.get("month")

    if not manager_id or not month:
        return Response(
            {"detail": "manager_id and month are required query params"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    summary = get_manager_summary(manager_id, month)
    if not summary:
        return Response({"detail": "Manager not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response(ManagerSummarySerializer(summary).data)
