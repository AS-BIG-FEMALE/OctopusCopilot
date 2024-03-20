import json
import os
import re
import time
import unittest

import azure.functions as func
from retry import retry
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

from function_app import copilot_handler_internal
from infrastructure.users import save_users_octopus_url_from_login, save_default_values
from tests.infrastructure.create_and_deploy_release import create_and_deploy_release
from tests.infrastructure.octopus_config import Octopus_Api_Key, Octopus_Url
from tests.infrastructure.octopus_infrastructure_test import run_terraform


class CopilotChatTest(unittest.TestCase):
    """
    End-to-end tests that verify the complete query workflow including:
    * Persisting user details such as Octopus URL and API key
    * Querying the Octopus API to build context
    * Passing the context and query to OpenAI to generate a response

    These tests are against a space with a small number of resources. They verify that basic context is successfully
    passed to the LLM and that the responses are valid.

    The answers provided by LLMs degrade with more complex contexts, so these tests are not exhaustive. But they do
    serve to validate the query workflow at a low level.
    """

    @classmethod
    def setUpClass(cls):
        # Simulate the result of a user login and saving their Octopus details
        try:
            save_users_octopus_url_from_login(os.environ["TEST_GH_USER"],
                                              Octopus_Url,
                                              Octopus_Api_Key,
                                              os.environ["ENCRYPTION_PASSWORD"],
                                              os.environ["ENCRYPTION_SALT"],
                                              os.environ["AzureWebJobsStorage"])
            save_default_values(os.environ["TEST_GH_USER"],
                                "space",
                                "Simple",
                                os.environ["AzureWebJobsStorage"])
            save_default_values(os.environ["TEST_GH_USER"],
                                "project",
                                "First Test Project",
                                os.environ["AzureWebJobsStorage"])
            save_default_values(os.environ["TEST_GH_USER"],
                                "environment",
                                "Development",
                                os.environ["AzureWebJobsStorage"])
        except Exception as e:
            print(
                "The tests will fail because Azurite is not running. Run Azureite with: "
                + "docker run -d -p 10000:10000 -p 10001:10001 -p 10002:10002 mcr.microsoft.com/azure-storage/azurite")
            return

        try:
            cls.mssql = DockerContainer("mcr.microsoft.com/mssql/server:2022-latest").with_env(
                "ACCEPT_EULA", "True").with_env("SA_PASSWORD", "Password01!")
            cls.mssql.start()
            wait_for_logs(cls.mssql, "SQL Server is now ready for client connections")

            mssql_ip = cls.mssql.get_docker_client().bridge_ip(cls.mssql.get_wrapped_container().id)

            cls.octopus = DockerContainer("octopusdeploy/octopusdeploy").with_bind_ports(8080, 8080).with_env(
                "ACCEPT_EULA", "Y").with_env("DB_CONNECTION_STRING",
                                             "Server=" + mssql_ip + ",1433;Database=OctopusDeploy;User=sa;Password=Password01!").with_env(
                "ADMIN_API_KEY", Octopus_Api_Key).with_env("DISABLE_DIND", "Y").with_env(
                "ADMIN_USERNAME", "admin").with_env("ADMIN_PASSWORD", "Password01!").with_env(
                "OCTOPUS_SERVER_BASE64_LICENSE", os.environ["LICENSE"])
            cls.octopus.start()
            wait_for_logs(cls.octopus, "Web server is ready to process requests")

            output = run_terraform("../terraform/simple/space_creation", Octopus_Url, Octopus_Api_Key)
            run_terraform("../terraform/simple/space_population", Octopus_Url, Octopus_Api_Key,
                          json.loads(output)["octopus_space_id"]["value"])
            run_terraform("../terraform/empty/space_creation", Octopus_Url, Octopus_Api_Key)
        except Exception as e:
            cls.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.octopus.stop()
        except Exception as e:
            pass
        finally:
            cls.octopus = None

        try:
            cls.mssql.stop()
        except Exception as e:
            pass
        finally:
            cls.mssql = None

    @retry(AssertionError, tries=3, delay=2)
    def test_get_variables(self):
        prompt = "List the variables defined in the project \"First Test Project\" in space \"Simple\"."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("Test.Variable" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_get_variables_with_defaults(self):
        prompt = "List the variables defined in the project."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("Test.Variable" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_step(self):
        prompt = "What does the step \"Run a Script\" do in the project \"First Test Project\" in space \"Simple\"."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("Hi there" in response_text, "The context must include details of the named step")

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_missing_step(self):
        prompt = "What does the project \"First Test Project\" in space \"Simple\"."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertFalse("Hi there" in response_text,
                         "The context should not include details of steps, because none were mentioned in the query")

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_machines(self):
        prompt = "What machines are in the space \"Simple\"."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("Cloud Region Target" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_all_projects(self):
        prompt = "What projects are in the space \"Simple\"."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("Runbook Project" in response_text)
        self.assertTrue("First Test Project" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_runbook(self):
        prompt = "What is the description of the \"Backup Database\" runbook in the \"Runbook Project\" project."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("Test Runbook" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_machine_policies(self):
        prompt = "Show the powershell health check script for the \"Windows VM Policy\" machine policy."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("win32_LogicalDisk" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_project_groups(self):
        prompt = "What is the description of the \"Azure Apps\" project group?"
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("Test Description" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_tenants(self):
        prompt = "Describe the tenant \"Marketing\"."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("Marketing" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_environment(self):
        prompt = "Does the \"Development\" environment allow dynamic infrastructure?."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("Development" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_feed(self):
        prompt = "What is the URI of the \"Helm\" feed?."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("https://charts.helm.sh/stable/" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_account(self):
        prompt = "What is the access key in the \"AWS Account\" account."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("ABCDEFGHIJKLMNOPQRST" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_variable_set(self):
        prompt = "List the variables belonging to the \"Database Settings\" library variable set."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("Test.Variable" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_worker_pool(self):
        prompt = "What is the description of the \"Docker\" worker pool?"
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("Workers running Docker containers" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_certificate(self):
        prompt = "What is the note of the \"Kind CA\" certificate?"
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("A test certificate" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_tagsets(self):
        prompt = "List the tags associated with the \"region\" tag set?"
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("us-east-1" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_lifecycle(self):
        prompt = "What environments are in the \"Simple\" lifecycle?"
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("Production" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_describe_git_creds(self):
        prompt = "What is the username for the \"GitHub Credentials\" git credentials?"
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue("admin" in response_text)

    @retry(AssertionError, tries=3, delay=2)
    def test_get_latest_deployment(self):
        create_and_deploy_release(space_name="Simple")
        prompt = "Get the release version of the latest deployment to the \"Development\" environment for the \"First Test Project\" project."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue(re.search("0\\.0\\.[1-9][0-9]*", response_text))

    @retry(AssertionError, tries=3, delay=2)
    def test_get_latest_deployment_defaults(self):
        create_and_deploy_release(space_name="Simple")
        prompt = "Get the release version of the latest deployment."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        self.assertTrue(re.search("0\\.0\\.[1-9][0-9]*", response_text))

    @retry(AssertionError, tries=3, delay=2)
    def test_general_question(self):
        prompt = "What does the project \"First Test Project\" do?"
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        # This response could be anything, but make sure the LLM isn't saying sorry for something.
        self.assertTrue("sorry" not in response_text.casefold())

    @retry(AssertionError, tries=3, delay=2)
    def test_get_logs(self):
        create_and_deploy_release(space_name="Simple")

        time.sleep(30)

        prompt = "List anything interesting in the deployment logs for the latest deployment."
        response = copilot_handler_internal(build_request(prompt))
        response_text = response.get_body().decode('utf8')

        # This response could be anything, but make sure the LLM isn't saying sorry for something.
        self.assertTrue("sorry" not in response_text.casefold())


if __name__ == '__main__':
    unittest.main()


def build_request(message):
    return func.HttpRequest(
        method='POST',
        body=json.dumps({
            "messages": [
                {
                    "content": message
                }
            ]
        }).encode('utf8'),
        url='/api/form_handler',
        params=None,
        headers={
            "X-GitHub-Token": os.environ["GH_TEST_TOKEN"]
        })
