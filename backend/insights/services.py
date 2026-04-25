import json
from functools import lru_cache
from pathlib import Path
from statistics import mean

DATA_FILE = Path(__file__).resolve().parent / "data" / "sample_data.json"


@lru_cache(maxsize=1)
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_avg(values):
    return round(mean(values), 2) if values else None


def get_developers():
    data = load_data()
    return sorted(data["developers"], key=lambda d: d["developer_name"])


def get_developer_by_id(developer_id):
    return next((d for d in get_developers() if d["developer_id"] == developer_id), None)


def get_managers():
    managers = {}
    for dev in get_developers():
        managers[dev["manager_id"]] = {
            "manager_id": dev["manager_id"],
            "manager_name": dev["manager_name"],
            "team_name": dev["team_name"],
        }
    return sorted(managers.values(), key=lambda m: m["manager_name"])


def get_manager_by_id(manager_id):
    return next((m for m in get_managers() if m["manager_id"] == manager_id), None)


def get_months():
    data = load_data()
    months = set()

    for row in data["jira_issues"]:
        months.add(row["month_done"])
    for row in data["pull_requests"]:
        months.add(row["month_merged"])
    for row in data["deployments"]:
        months.add(row["month_deployed"])
    for row in data["bugs"]:
        months.add(row["month_found"])

    return sorted(months)


def get_issues_for_developer_month(developer_id, month):
    data = load_data()
    return [
        issue for issue in data["jira_issues"]
        if issue["developer_id"] == developer_id
        and issue["month_done"] == month
        and issue["status"] == "Done"
    ]


def get_prs_for_developer_month(developer_id, month):
    data = load_data()
    return [
        pr for pr in data["pull_requests"]
        if pr["developer_id"] == developer_id
        and pr["month_merged"] == month
        and pr["status"] == "merged"
    ]


def get_deployments_for_developer_month(developer_id, month):
    data = load_data()
    return [
        dep for dep in data["deployments"]
        if dep["developer_id"] == developer_id
        and dep["month_deployed"] == month
        and dep["status"] == "success"
        and dep["environment"] == "prod"
    ]


def get_bugs_for_developer_month(developer_id, month):
    data = load_data()
    return [
        bug for bug in data["bugs"]
        if bug["developer_id"] == developer_id
        and bug["month_found"] == month
        and bug["escaped_to_prod"] == "Yes"
    ]


def get_org_avg_review_wait(month):
    data = load_data()
    prs = [pr for pr in data["pull_requests"] if pr["month_merged"] == month and pr["status"] == "merged"]
    return safe_avg([pr["review_wait_hours"] for pr in prs])


def calculate_ic_metrics(developer_id, month):
    issues = get_issues_for_developer_month(developer_id, month)
    prs = get_prs_for_developer_month(developer_id, month)
    deployments = get_deployments_for_developer_month(developer_id, month)
    bugs = get_bugs_for_developer_month(developer_id, month)

    issues_done = len(issues)
    escaped_bugs = len(bugs)

    bug_rate = round((escaped_bugs / issues_done), 2) if issues_done else 0
    bug_rate_pct = round(bug_rate * 100, 0)

    return {
        "issues_done": issues_done,
        "merged_prs": len(prs),
        "prod_deployments": len(deployments),
        "escaped_bugs": escaped_bugs,
        "avg_cycle_time_days": safe_avg([issue["cycle_time_days"] for issue in issues]),
        "avg_lead_time_days": safe_avg([dep["lead_time_days"] for dep in deployments]),
        "bug_rate": bug_rate,
        "bug_rate_pct": bug_rate_pct,
        "avg_review_wait_hours": safe_avg([pr["review_wait_hours"] for pr in prs]),
        "avg_lines_changed": safe_avg([pr["lines_changed"] for pr in prs]),
        "avg_story_points": safe_avg([issue["story_points"] for issue in issues]),
        "root_causes": sorted(list({bug["root_cause_bucket"] for bug in bugs})),
    }


def generate_pattern_hint(metrics, month):
    lead = metrics["avg_lead_time_days"]
    cycle = metrics["avg_cycle_time_days"]
    bug_rate = metrics["bug_rate"]
    review_wait = metrics["avg_review_wait_hours"]
    deployments = metrics["prod_deployments"]
    org_review_avg = get_org_avg_review_wait(month)

    if bug_rate > 0:
        return "Quality watch"

    if (
        review_wait is not None
        and org_review_avg is not None
        and review_wait > org_review_avg + 3
    ):
        return "Review bottleneck"

    if (
        lead is not None
        and cycle is not None
        and lead - cycle > 1
    ):
        return "Deployment delay"

    if (
        lead is not None
        and cycle is not None
        and lead < 4
        and cycle < 5
        and bug_rate == 0
        and deployments >= 2
    ):
        return "Healthy flow"

    return "Needs review"


def generate_evidence(metrics, month):
    evidence = []

    if metrics["avg_review_wait_hours"] is not None:
        evidence.append(f"Average review wait: {metrics['avg_review_wait_hours']} hours")

    if metrics["avg_lines_changed"] is not None:
        evidence.append(f"Average PR size: {metrics['avg_lines_changed']} lines changed")

    if metrics["avg_story_points"] is not None:
        evidence.append(f"Average issue size: {metrics['avg_story_points']} story points")

    if metrics["root_causes"]:
        evidence.append("Escaped bug root causes: " + ", ".join(metrics["root_causes"]))

    org_review_avg = get_org_avg_review_wait(month)
    if org_review_avg is not None:
        evidence.append(f"Org average review wait in {month}: {org_review_avg} hours")

    return evidence[:4]


def generate_interpretation(metrics, month):
    lead = metrics["avg_lead_time_days"]
    cycle = metrics["avg_cycle_time_days"]
    bug_rate_pct = metrics["bug_rate_pct"]
    bugs = metrics["escaped_bugs"]
    deployments = metrics["prod_deployments"]
    prs = metrics["merged_prs"]
    review_wait = metrics["avg_review_wait_hours"]
    org_review_avg = get_org_avg_review_wait(month)

    if bug_rate_pct > 0:
        return (
            f"You are shipping regularly, with {deployments} production deployments and {prs} merged PRs this month, "
            f"but quality needs attention. {bugs} completed issue(s) led to escaped production bugs, which makes your "
            f"bug rate {int(bug_rate_pct)}%. Your cycle time is {cycle} days, so the main concern looks less like raw "
            f"delivery speed and more like quality and work-shaping."
        )

    if (
        review_wait is not None
        and org_review_avg is not None
        and review_wait > org_review_avg + 3
    ):
        return (
            f"Your coding flow looks reasonable, but reviews are taking longer than the monthly average. "
            f"With review wait at {review_wait} hours versus an org average of {org_review_avg} hours, "
            f"code review may be the main bottleneck slowing your path to merge."
        )

    if lead is not None and cycle is not None and lead - cycle > 1:
        return (
            f"Your work completes in about {cycle} days, but it reaches production in about {lead} days. "
            f"That extra delay after implementation suggests a release or deployment bottleneck rather than a coding bottleneck."
        )

    if lead is not None and cycle is not None and lead < 4 and cycle < 5 and bug_rate_pct == 0 and deployments >= 2:
        return (
            f"Your delivery flow looks healthy. Work moves from in-progress to done in about {cycle} days, "
            f"reaches production in about {lead} days, and you shipped {deployments} successful production deployments "
            f"with no escaped bugs."
        )

    return (
        f"Your month shows a mixed but understandable delivery pattern. You are shipping work, but the current metric mix "
        f"suggests there is at least one area to monitor more closely: scope, review turnaround, or release flow."
    )


def generate_next_steps(metrics, month):
    steps = []

    if metrics["bug_rate"] > 0:
        if "test gap" in metrics["root_causes"]:
            steps.append({
                "title": "Strengthen test coverage",
                "description": "A production bug was tagged as a test gap, so add edge-case and regression checks before the next release."
            })
        elif "edge case" in metrics["root_causes"]:
            steps.append({
                "title": "Add explicit edge-case testing",
                "description": "Recent escaped bugs point to edge-case handling, so add targeted tests for less common user paths."
            })
        else:
            steps.append({
                "title": "Add one release-quality safeguard",
                "description": "This month had escaped bugs, so add one lightweight quality gate such as a release checklist, peer walkthrough, or regression pass."
            })

    if metrics["avg_cycle_time_days"] is not None and metrics["avg_cycle_time_days"] > 5:
        steps.append({
            "title": "Reduce work item size",
            "description": "Your cycle time is elevated, so try breaking larger stories or tasks into smaller chunks to get feedback earlier."
        })

    org_review_avg = get_org_avg_review_wait(month)
    if (
        metrics["avg_review_wait_hours"] is not None
        and org_review_avg is not None
        and metrics["avg_review_wait_hours"] > org_review_avg + 3
    ):
        steps.append({
            "title": "Speed up review turnaround",
            "description": "Ask for review earlier, keep PRs smaller where possible, and request feedback proactively on changes likely to block release."
        })

    if (
        metrics["avg_lead_time_days"] is not None
        and metrics["avg_cycle_time_days"] is not None
        and metrics["avg_lead_time_days"] - metrics["avg_cycle_time_days"] > 1
    ):
        steps.append({
            "title": "Investigate post-code delay",
            "description": "There is noticeable time between implementation and production, so check whether release batching or deployment flow is slowing delivery."
        })

    if not steps:
        steps.extend([
            {
                "title": "Maintain your current flow",
                "description": "Your metrics suggest a healthy month. Keep the same working rhythm and watch for any changes next month."
            },
            {
                "title": "Document what works well",
                "description": "Capture the habits that helped you ship smoothly so they can be reused or shared across the team."
            },
            {
                "title": "Track the trend next month",
                "description": "Healthy months matter most when they repeat, so compare this pattern against the next month before making changes."
            },
        ])

    return steps[:3]


def get_ic_insight(developer_id, month):
    developer = get_developer_by_id(developer_id)
    if not developer:
        return None

    metrics = calculate_ic_metrics(developer_id, month)
    return {
        "developer_id": developer["developer_id"],
        "developer_name": developer["developer_name"],
        "team_name": developer["team_name"],
        "manager_name": developer["manager_name"],
        "month": month,
        "pattern_hint": generate_pattern_hint(metrics, month),
        "interpretation": generate_interpretation(metrics, month),
        "evidence": generate_evidence(metrics, month),
        "metrics": metrics,
        "next_steps": generate_next_steps(metrics, month),
    }


def generate_manager_signal(team_metrics):
    if team_metrics["bug_rate_pct"] > 0:
        return "Watch quality"
    if (
        team_metrics["avg_lead_time_days"] is not None
        and team_metrics["avg_cycle_time_days"] is not None
        and team_metrics["avg_lead_time_days"] < 4
        and team_metrics["avg_cycle_time_days"] < 5
    ):
        return "Healthy flow"
    return "Watch bottlenecks"


def get_manager_summary(manager_id, month):
    manager = get_manager_by_id(manager_id)
    if not manager:
        return None

    members = [dev for dev in get_developers() if dev["manager_id"] == manager_id]
    developer_rows = []
    total_issues = 0
    total_bugs = 0
    total_prs = 0
    total_deployments = 0
    lead_values = []
    cycle_values = []

    for dev in members:
        insight = get_ic_insight(dev["developer_id"], month)
        metrics = insight["metrics"]

        total_issues += metrics["issues_done"]
        total_bugs += metrics["escaped_bugs"]
        total_prs += metrics["merged_prs"]
        total_deployments += metrics["prod_deployments"]

        if metrics["avg_lead_time_days"] is not None:
            lead_values.append(metrics["avg_lead_time_days"])
        if metrics["avg_cycle_time_days"] is not None:
            cycle_values.append(metrics["avg_cycle_time_days"])

        developer_rows.append({
            "developer_id": dev["developer_id"],
            "developer_name": dev["developer_name"],
            "pattern_hint": insight["pattern_hint"],
            "avg_cycle_time_days": metrics["avg_cycle_time_days"],
            "avg_lead_time_days": metrics["avg_lead_time_days"],
            "bug_rate_pct": metrics["bug_rate_pct"],
            "prod_deployments": metrics["prod_deployments"],
            "merged_prs": metrics["merged_prs"],
        })

    team_metrics = {
        "issues_done": total_issues,
        "escaped_bugs": total_bugs,
        "merged_prs": total_prs,
        "prod_deployments": total_deployments,
        "avg_cycle_time_days": safe_avg(cycle_values),
        "avg_lead_time_days": safe_avg(lead_values),
        "bug_rate_pct": round((total_bugs / total_issues) * 100, 0) if total_issues else 0,
    }

    return {
        "manager_id": manager["manager_id"],
        "manager_name": manager["manager_name"],
        "team_name": manager["team_name"],
        "month": month,
        "team_size": len(members),
        "team_signal": generate_manager_signal(team_metrics),
        "team_metrics": team_metrics,
        "developers": developer_rows,
    }
