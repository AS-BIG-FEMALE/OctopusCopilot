import asyncio

from domain.logging.app_logging import configure_logging
from domain.lookup.octopus_lookups import lookup_space, lookup_projects
from domain.response.copilot_response import CopilotResponse
from domain.tools.debug import get_params_message
from domain.transformers.chat_responses import get_project_dashboard_response, get_project_tenant_progression_response
from infrastructure.github import get_workflow_run_async
from infrastructure.octopus import get_project, get_project_progression, \
    get_project_tenant_dashboard, get_release_github_workflow_async

logger = configure_logging(__name__)


def get_project_dashboard_callback(github_user, github_token, log_query=None):
    def get_project_dashboard_callback_implementation(original_query, api_key, url, space_name, project_name):
        debug_text = get_params_message(github_user, True,
                                        get_project_dashboard_callback_implementation.__name__,
                                        original_query=original_query,
                                        space_name=space_name,
                                        project_name=project_name)
        space_id, space_name, warnings = lookup_space(url, api_key, github_user, original_query, space_name)
        sanitized_project_names, sanitized_projects = lookup_projects(url, api_key, github_user, original_query,
                                                                      space_id, project_name)

        if not sanitized_project_names:
            return CopilotResponse("Please specify a project name in the query.")

        if log_query:
            log_query("get_project_dashboard_callback_implementation", f"""
                Space: {space_name}
                Project Names: {sanitized_project_names[0]}""")

        debug_text.extend(get_params_message(github_user, False,
                                             get_project_dashboard_callback_implementation.__name__,
                                             original_query=original_query,
                                             space_name=space_name,
                                             project_name=sanitized_project_names[0]))

        project = get_project(space_id, sanitized_project_names[0], api_key, url)

        response = []
        if project["TenantedDeploymentMode"] == "Untenanted":
            response.append(get_dashboard(space_id, space_name, project, api_key, url, github_token))
        else:
            response.append(get_tenanted_dashboard(space_id, space_name, project, api_key, url, github_token))

        response.extend(warnings)
        response.extend(debug_text)

        return CopilotResponse("\n\n".join(response))

    return get_project_dashboard_callback_implementation


def get_dashboard(space_id, space_name, project, api_key, url, github_token):
    progression = get_project_progression(space_id, project["Id"], api_key, url)

    try:
        release_workflows = asyncio.run(get_dashboard_release_workflows(space_id, progression, api_key, url))
        release_workflow_runs = asyncio.run(get_release_workflow_runs(release_workflows, github_token))
    except Exception as e:
        logger.error(e)
        release_workflow_runs = None

    return get_project_dashboard_response(space_name, project["Name"], progression, release_workflow_runs)


async def get_tenanted_dashboard_release_workflows(space_id, progression, api_key, url):
    """
    Return the details of the associated GitHub workflow from the release notes of each release.
    """
    return await asyncio.gather(
        *[get_release_github_workflow_async(space_id, x["ReleaseId"], api_key, url) for x in
          progression["Items"]])


async def get_dashboard_release_workflows(space_id, progression, api_key, url):
    """
    Return the details of the associated GitHub workflow from the release notes of each release.
    """
    return await asyncio.gather(
        *[get_release_github_workflow_async(space_id, x["Release"]["Id"], api_key, url) for x in
          progression["Releases"]])


async def get_release_workflow_runs(release_workflows, github_token):
    """
    Return the status of the workflow runs for each release.
    """
    return await asyncio.gather(
        *[get_workflow_status(x["ReleaseId"], x["Owner"], x["Repo"], x["RunId"], github_token) for x in
          release_workflows])


async def get_workflow_status(release_id, owner, repo, run_id, github_token):
    try:
        workflow = await get_workflow_run_async(owner, repo, run_id, github_token)
        return {"ReleaseId": release_id,
                "Status": workflow.get("status"),
                "Conclusion": workflow.get("conclusion"),
                "Sha": workflow.get("head_sha"),
                "ShortSha": workflow.get("head_sha")[:7],
                "Name": workflow.get("name"),
                "Url": workflow.get("html_url")}
    except Exception as e:
        # Silent fail, and fall back to returning blank result
        logger.error(e)
    return {"ReleaseId": release_id, "Status": "", "Sha": "", "Name": "", "Url": "", "ShortSha": ""}


def get_tenanted_dashboard(space_id, space_name, project, api_key, url, github_token):
    progression = get_project_tenant_dashboard(space_id, project["Id"], api_key, url)

    try:
        release_workflows = asyncio.run(
            get_tenanted_dashboard_release_workflows(space_id, progression["Dashboard"], api_key, url))
        release_workflow_runs = asyncio.run(get_release_workflow_runs(release_workflows, github_token))
    except Exception as e:
        logger.error(e)
        release_workflow_runs = None

    return get_project_tenant_progression_response(space_id,
                                                   space_name,
                                                   project["Name"],
                                                   project["Id"],
                                                   progression["Dashboard"],
                                                   release_workflow_runs,
                                                   api_key, url)
