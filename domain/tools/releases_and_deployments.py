def answer_releases_and_deployments_callback(original_query, callback, logging):
    def answer_releases_and_deployments_usage(space=None, projects=None, environments=None, channels=None,
                                              releases=None, **kwargs):
        """Answers a question about deployments and releases.

        Args:
        space: Space name
        projects: project names
        environments: variable names
        channels: chanel names
        releases: release versions
        """

        # Build a few shot sample query with a chain-of-thought example to help the LLM understand the relationships
        # between projects, releases, deployments, and environments

        few_shot = f"""
Task: Given the HCL representation of a project and environment; and a JSON representation of deployments and release, what is the release version of the latest deployment of the "My Project" project to the "Production" environment for the "Default" channel and the "My Tenant" tenant?

Example 1:
HCL: ###
resource "octopusdeploy_environment" "environment_production" {{
  id                           = "Environments-6789"
  name                         = "Production"
}}
resource "octopusdeploy_project" "test_project" {{
    id = "Projects-1234"
    name = "My Project"
}}
resource "octopusdeploy_tenant" "my_tenant" {{
  id = "Tenants-234"
  name = "My Tenant"
}}
resource "octopusdeploy_channel" "default" {{
  id = "Channels-7001"
  name = "Default"
}}
###
JSON: ###
{{
  "Environments": [
    {{
      "Id": "Environments-6789",
      "Name": "Production"
    }},
    {{
      "Id": "Environments-3023",
      "Name": "Security"
    }}
  ],
  "Releases": [
    {{
      "Release": {{
        "Id": "Releases-13568",
        "SpaceId": "Spaces-2328",
        "ProjectId": "Projects-1234",
        "Version": "1.2.3-mybranch",
        "ChannelId": "Channels-7001",
      }},
      "Deployments": {{
        "Environments-6789": [
          {{
            "Id": "Deployments-16435",
            "ProjectId": "Projects-1234",
            "EnvironmentId": "Environments-6789",
            "ReleaseId": "Releases-13568",
            "DeploymentId": "Deployments-16435",
            "TaskId": "ServerTasks-701983",
            "TenantId": "Tenants-234",
            "ChannelId": "Channels-7001",
            "ReleaseVersion": "1.2.3-mybranch",
            "Created": "2024-03-13T04:07:59.537+00:00",
            "QueueTime": "2024-03-13T04:07:59.537+00:00",
            "StartTime": "2024-03-13T04:08:00.196+00:00",
            "CompletedTime": "2024-03-13T04:08:47.885+00:00",
            "State": "Success",
          }}
        ]
      }}
    }},
    {{
      "Release": {{
        "Id": "Releases-13546",
        "SpaceId": "Spaces-2328",
        "ProjectId": "Projects-1234",
        "Version": "0.1.1049+run970-attempt1",
        "ChannelId": "Channels-7001",
      }},
      "Deployments": {{
        "Environments-6789": [
          {{
            "Id": "Deployments-16406",
            "ProjectId": "Projects-1234",
            "EnvironmentId": "Environments-6789",
            "ReleaseId": "Releases-13546",
            "DeploymentId": "Deployments-16406",
            "TaskId": "ServerTasks-700878",
            "TenantId": null,
            "ChannelId": "Channels-7001",
            "ReleaseVersion": "0.1.1049+run970-attempt1",
            "Created": "2024-03-11T23:41:10.241+00:00",
            "QueueTime": "2024-03-11T23:41:10.241+00:00",
            "StartTime": "2024-03-11T23:41:11.125+00:00",
            "CompletedTime": "2024-03-11T23:42:04.328+00:00",
            "State": "Success"
          }}
        ]
      }}
    }},
    {{
      "Release": {{
        "Id": "Releases-13382",
        "SpaceId": "Spaces-2328",
        "ProjectId": "Projects-1234",
        "Version": "0.1.981+run900-attempt1",
        "ChannelId": "Channels-7001",
      }},
      "Deployments": {{
        "Environments-6789": [
          {{
            "Id": "Deployments-16139",
            "ProjectId": "Projects-1234",
            "EnvironmentId": "Environments-6789",
            "ReleaseId": "Releases-13382",
            "DeploymentId": "Deployments-16139",
            "TaskId": "ServerTasks-694793",
            "TenantId": null,
            "ChannelId": "Channels-7001",
            "ReleaseVersion": "0.1.981+run900-attempt1",
            "Created": "2024-03-05T13:01:12.534+00:00",
            "QueueTime": "2024-03-05T13:01:12.534+00:00",
            "StartTime": "2024-03-05T13:01:13.200+00:00",
            "CompletedTime": "2024-03-05T13:02:21.218+00:00",
            "State": "Success"
          }}
        ],
        "Environments-3023": [
          {{
            "Id": "Deployments-16457",
            "ProjectId": "Projects-1234",
            "EnvironmentId": "Environments-3023",
            "ReleaseId": "Releases-13382",
            "DeploymentId": "Deployments-16457",
            "TaskId": "ServerTasks-702237",
            "TenantId": null,
            "ChannelId": "Channels-7001",
            "ReleaseVersion": "0.1.981+run900-attempt1",
            "Created": "2024-03-13T09:00:24.957+00:00",
            "QueueTime": "2024-03-13T09:00:24.957+00:00",
            "StartTime": "2024-03-13T09:00:25.871+00:00",
            "CompletedTime": "2024-03-13T09:01:50.618+00:00",
            "State": "Success"
          }},
          {{
            "Id": "Deployments-16418",
            "ProjectId": "Projects-1234",
            "EnvironmentId": "Environments-3023",
            "ReleaseId": "Releases-13382",
            "DeploymentId": "Deployments-16418",
            "TaskId": "ServerTasks-701289",
            "TenantId": null,
            "ChannelId": "Channels-7001",
            "ReleaseVersion": "0.1.981+run900-attempt1",
            "Created": "2024-03-12T09:00:11.711+00:00",
            "QueueTime": "2024-03-12T09:00:11.711+00:00",
            "StartTime": "2024-03-12T09:00:12.800+00:00",
            "CompletedTime": "2024-03-12T09:01:38.999+00:00",
            "State": "Success",
          }},
          {{
            "Id": "Deployments-16384",
            "ProjectId": "Projects-1234",
            "EnvironmentId": "Environments-3023",
            "ReleaseId": "Releases-13382",
            "DeploymentId": "Deployments-16384",
            "TaskId": "ServerTasks-700271",
            "TenantId": null,
            "ChannelId": "Channels-7001",
            "ReleaseVersion": "0.1.981+run900-attempt1",
            "Created": "2024-03-11T09:00:21.952+00:00",
            "QueueTime": "2024-03-11T09:00:21.952+00:00",
            "StartTime": "2024-03-11T09:00:22.879+00:00",
            "CompletedTime": "2024-03-11T09:01:39.194+00:00",
            "State": "Success",
          }},
          {{
            "Id": "Deployments-16334",
            "ProjectId": "Projects-1234",
            "EnvironmentId": "Environments-3023",
            "ReleaseId": "Releases-13382",
            "DeploymentId": "Deployments-16334",
            "TaskId": "ServerTasks-699290",
            "TenantId": null,
            "ChannelId": "Channels-7001",
            "ReleaseVersion": "0.1.981+run900-attempt1",
            "Created": "2024-03-10T09:00:27.185+00:00",
            "QueueTime": "2024-03-10T09:00:27.185+00:00",
            "StartTime": "2024-03-10T09:00:28.171+00:00",
            "CompletedTime": "2024-03-10T09:01:31.152+00:00",
            "State": "Success",
          }},
          {{
            "Id": "Deployments-16302",
            "ProjectId": "Projects-1234",
            "EnvironmentId": "Environments-3023",
            "ReleaseId": "Releases-13382",
            "DeploymentId": "Deployments-16302",
            "TaskId": "ServerTasks-698372",
            "TenantId": null,
            "ChannelId": "Channels-7001",
            "ReleaseVersion": "0.1.981+run900-attempt1",
            "Created": "2024-03-09T09:00:24.699+00:00",
            "QueueTime": "2024-03-09T09:00:24.699+00:00",
            "StartTime": "2024-03-09T09:00:25.475+00:00",
            "CompletedTime": "2024-03-09T09:01:24.656+00:00",
            "State": "Success",
          }},
          {{
            "Id": "Deployments-16290",
            "ProjectId": "Projects-1234",
            "EnvironmentId": "Environments-3023",
            "ReleaseId": "Releases-13382",
            "DeploymentId": "Deployments-16290",
            "TaskId": "ServerTasks-697471",
            "TenantId": null,
            "ChannelId": "Channels-7001",
            "ReleaseVersion": "0.1.981+run900-attempt1",
            "Created": "2024-03-08T09:00:09.494+00:00",
            "QueueTime": "2024-03-08T09:00:09.494+00:00",
            "StartTime": "2024-03-08T09:00:10.264+00:00",
            "CompletedTime": "2024-03-08T09:01:30.781+00:00",
            "State": "Success",
          }},
          {{
            "Id": "Deployments-16253",
            "ProjectId": "Projects-1234",
            "EnvironmentId": "Environments-3023",
            "ReleaseId": "Releases-13382",
            "DeploymentId": "Deployments-16253",
            "TaskId": "ServerTasks-696535",
            "TenantId": null,
            "ChannelId": "Channels-7001",
            "ReleaseVersion": "0.1.981+run900-attempt1",
            "Created": "2024-03-07T09:00:15.120+00:00",
            "QueueTime": "2024-03-07T09:00:15.120+00:00",
            "StartTime": "2024-03-07T09:00:16.056+00:00",
            "CompletedTime": "2024-03-07T09:01:36.054+00:00",
            "State": "Success",
          }},
          {{
            "Id": "Deployments-16189",
            "ProjectId": "Projects-1234",
            "EnvironmentId": "Environments-3023",
            "ReleaseId": "Releases-13382",
            "DeploymentId": "Deployments-16189",
            "TaskId": "ServerTasks-695588",
            "TenantId": null,
            "ChannelId": "Channels-7001",
            "ReleaseVersion": "0.1.981+run900-attempt1",
            "Created": "2024-03-06T09:00:20.152+00:00",
            "QueueTime": "2024-03-06T09:00:20.152+00:00",
            "StartTime": "2024-03-06T09:00:21.011+00:00",
            "CompletedTime": "2024-03-06T09:02:47.565+00:00",
            "State": "Success",
          }},
          {{
            "Id": "Deployments-16140",
            "ProjectId": "Projects-1234",
            "EnvironmentId": "Environments-3023",
            "ReleaseId": "Releases-13382",
            "DeploymentId": "Deployments-16140",
            "TaskId": "ServerTasks-694794",
            "TenantId": null,
            "ChannelId": "Channels-7001",
            "ReleaseVersion": "0.1.981+run900-attempt1",
            "Created": "2024-03-05T13:02:21.381+00:00",
            "QueueTime": "2024-03-05T13:02:21.381+00:00",
            "StartTime": "2024-03-05T13:02:21.920+00:00",
            "CompletedTime": "2024-03-05T13:03:15.097+00:00",
            "State": "Success",
          }}
        ]
      }}
    }}
  ]
}}
###
Output:
The HCL resource with the labels "octopusdeploy_environment" and "environment_production" has an attribute called "name" with the value "Production" and an "id" with the value "Environments-6789". This name matches the environment name in the query. Therefore, this is the environment we base the answer on.
The HCL resource with the labels "octopusdeploy_project" and "test_project" has an attribute called "name" with the value "My Project" and an "id" with the value "Projects-1234". This name matches the project name in the query. Therefore, this is the project we base the answer on.
The HCL resource with the labels "octopusdeploy_tenant" and "my_tenant" has an attribute called "name" with the value "My Tenant" and an "id" of "Tenants-234". This name matches the tenant name in the query. Therefore, this is the tenant we base the answer on.
The HCL resource with the labels "octopusdeploy_channel" and "default" has an attribute called "name" with the value "Default" and an "id" of "Channels-7001". This name matches the channel name in the query. Therefore, this is the channel we base the answer on.
The JSON blob has a property called "Releases" which is an array of release objects. Each release object has a property called "Release" with an attribute called "ProjectId" with the value "Projects-1234" that matches the "id" of the project called "My Project". Therefore, this is a release we can consider for the answer.
The release object has a property called "Deployments" which is an object mapping environment ids to deployments called an "environment deployment". The "Deployments" object includes an "environment deployment" with the id of "Environments-6789" that matches the "id" of environment "Production". Therefore, this "environment deployment" is one we can consider for the answer.
The "environment deployment" object has a "ProjectId" attribute with the value of "Projects-1234" that matches the "id" of the project "My Project". Therefore, this "environment deployment" is one we can consider for the answer.
The "environment deployment" object has a "TenantId" attribute with the value of "Tenants-234" that matches the "id" of the tenant "My Tenant". Therefore, this "environment deployment" is one we can consider for the answer.
The "environment deployment" object has a "ChannelId" attribute with the value of "Channels-7001" that matches the "id" of the channel "Default". Therefore, this "environment deployment" is one we can consider for the answer.
The "environment deployment" object with the highest "StartTime" attribute is the latest deployment. The release version is found in the "ReleaseVersion" attribute.
Therefore, the release version of the latest deployment of the "My Project" project to the "Production" environment is "1.2.3-mybranch".

The answer:
The release version of the latest deployment of the "My Project" project to the "Production" environment is "1.2.3-mybranch"

Question: {original_query}
"""

        for key, value in kwargs.items():
            if logging:
                logging(f"Unexpected Key: {key}", "Value: {value}")

        return callback(original_query, few_shot, space, projects, environments, channels, releases)

    return answer_releases_and_deployments_usage