from domain.response.copilot_response import CopilotResponse
from infrastructure.users import delete_user_details


def logout(github_user, connection_string):
    def logout_implementation():
        """Logs out or signs out the user
        """

        delete_user_details(github_user, connection_string)

        return CopilotResponse(f"Sign out successful")

    return logout_implementation
