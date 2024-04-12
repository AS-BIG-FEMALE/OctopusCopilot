def exclude_all_targets(query, entity_list):
    return True if (not entity_list
                    and "target" not in query.lower()
                    and "machine" not in query.lower()
                    and "agent" not in query.lower()
                    and "listening" not in query.lower()
                    and "ssh" not in query.lower()
                    and "cloud region" not in query.lower()
                    and "cloudregion" not in query.lower()
                    and "kubernetes" not in query.lower()
                    and "ecs" not in query.lower()
                    and "web app" not in query.lower()
                    and "webapp" not in query.lower()
                    and "service fabric" not in query.lower()
                    and "servicefabric" not in query.lower()
                    and "polling" not in query.lower()) else False


def exclude_all_runbooks(query, entity_list):
    return True if not entity_list and "runbook" not in query.lower() else False


def exclude_all_tenants(query, entity_list):
    return True if not entity_list and "tenant" not in query.lower() else False


def exclude_all_projects(query, entity_list):
    return True if not entity_list and "project" not in query.lower() else False


def exclude_all_library_variable_sets(query, entity_list):
    return True if not entity_list and "library variable set" not in query.lower() else False


def exclude_all_environments(query, entity_list):
    if entity_list and "<all>" in entity_list:
        return False
    return True if not entity_list and "environment" not in query.lower() else False


def exclude_all_feeds(query, entity_list):
    return True if not entity_list and "feed" not in query.lower() else False


def exclude_all_accounts(query, entity_list):
    return True if not entity_list and "account" not in query.lower() else False


def exclude_all_certificates(query, entity_list):
    return True if not entity_list and "certificate" not in query.lower() else False


def exclude_all_lifecycles(query, entity_list):
    return True if not entity_list and "lifecycle" not in query.lower() else False


def exclude_all_worker_pools(query, entity_list):
    return True if not entity_list and "worker pool" not in query.lower() else False


def exclude_all_machine_policies(query, entity_list):
    return True if not entity_list and "policy" not in query.lower() else False


def exclude_all_tagsets(query, entity_list):
    return True if not entity_list and "tag" not in query.lower() else False


def exclude_all_project_groups(query, entity_list):
    return True if not entity_list and "group" not in query.lower() else False


def exclude_all_steps(query, entity_list):
    return True if not entity_list and "step" not in query.lower() else False


def exclude_all_variables(query, entity_list):
    if entity_list and "<all>" in entity_list:
        return False
    return True if not entity_list and "variable" not in query.lower() else False


def release_is_latest(release_version):
    phrases = ["latest", "last", "most recent"]
    return not release_version or not release_version.strip() or release_version.casefold() in phrases
