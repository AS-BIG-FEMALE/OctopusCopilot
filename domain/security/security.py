import collections
import json
import logging

from domain.errors.error_handling import handle_error
from domain.exceptions.not_authorized import NotAuthorized


def is_admin_user(user, get_admin_users, callback):
    """
    A wrapper function that checks to see if the user is an admin. If so, the callback is called. If not, an exception is raised.
    :param user: A function returning the current user
    :param get_admin_users: A function returning a JSON list of users
    :param callback: The function to call if the user is authorized
    :return: The value returned by the callback
    """

    if not get_admin_users or not isinstance(get_admin_users, str) or not get_admin_users.strip():
        raise NotAuthorized()

    if not user or not isinstance(user, str) or not user.strip():
        raise NotAuthorized()

    if not callback:
        return

    try:
        admin_users = list(map(lambda x: str(x), json.loads(get_admin_users)))

        if not isinstance(admin_users, collections.abc.Sequence):
            raise Exception()

    except Exception as e:
        handle_error(e)
        raise NotAuthorized()

    if str(user) not in admin_users:
        logging.error(f"User {user} not found in {admin_users}")
        raise NotAuthorized()

    return callback()