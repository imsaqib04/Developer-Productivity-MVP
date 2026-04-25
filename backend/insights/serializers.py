from rest_framework import serializers


class DeveloperSerializer(serializers.Serializer):
    developer_id = serializers.CharField()
    developer_name = serializers.CharField()
    manager_id = serializers.CharField()
    manager_name = serializers.CharField()
    team_name = serializers.CharField()
    service_type = serializers.CharField()
    level = serializers.CharField()


class ManagerSerializer(serializers.Serializer):
    manager_id = serializers.CharField()
    manager_name = serializers.CharField()
    team_name = serializers.CharField()


class IcMetricsSerializer(serializers.Serializer):
    issues_done = serializers.IntegerField()
    merged_prs = serializers.IntegerField()
    prod_deployments = serializers.IntegerField()
    escaped_bugs = serializers.IntegerField()
    avg_cycle_time_days = serializers.FloatField(allow_null=True)
    avg_lead_time_days = serializers.FloatField(allow_null=True)
    bug_rate = serializers.FloatField()
    bug_rate_pct = serializers.FloatField()
    avg_review_wait_hours = serializers.FloatField(allow_null=True)
    avg_lines_changed = serializers.FloatField(allow_null=True)
    avg_story_points = serializers.FloatField(allow_null=True)
    root_causes = serializers.ListField(child=serializers.CharField())


class NextStepSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()


class IcInsightSerializer(serializers.Serializer):
    developer_id = serializers.CharField()
    developer_name = serializers.CharField()
    team_name = serializers.CharField()
    manager_name = serializers.CharField()
    month = serializers.CharField()
    pattern_hint = serializers.CharField()
    interpretation = serializers.CharField()
    evidence = serializers.ListField(child=serializers.CharField())
    metrics = IcMetricsSerializer()
    next_steps = NextStepSerializer(many=True)


class ManagerMemberSerializer(serializers.Serializer):
    developer_id = serializers.CharField()
    developer_name = serializers.CharField()
    pattern_hint = serializers.CharField()
    avg_cycle_time_days = serializers.FloatField(allow_null=True)
    avg_lead_time_days = serializers.FloatField(allow_null=True)
    bug_rate_pct = serializers.FloatField()
    prod_deployments = serializers.IntegerField()
    merged_prs = serializers.IntegerField()


class ManagerTeamMetricsSerializer(serializers.Serializer):
    issues_done = serializers.IntegerField()
    escaped_bugs = serializers.IntegerField()
    merged_prs = serializers.IntegerField()
    prod_deployments = serializers.IntegerField()
    avg_cycle_time_days = serializers.FloatField(allow_null=True)
    avg_lead_time_days = serializers.FloatField(allow_null=True)
    bug_rate_pct = serializers.FloatField()


class ManagerSummarySerializer(serializers.Serializer):
    manager_id = serializers.CharField()
    manager_name = serializers.CharField()
    team_name = serializers.CharField()
    month = serializers.CharField()
    team_size = serializers.IntegerField()
    team_signal = serializers.CharField()
    team_metrics = ManagerTeamMetricsSerializer()
    developers = ManagerMemberSerializer(many=True)
