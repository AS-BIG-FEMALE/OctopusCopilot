"""
This package holds callback functions called by wrappers.

The callback function may itself be returned by a callback wrapper. The callback wrapper captures platform specific
details, like a GitHub username, that can then be consumed by the callback.

This allows the wrapper to call a platform-agnostic callback function (i.e. a callback function without platform specific
arguments, like the GitHub username), while allowing the callback function to be aware of a specific platform.

This package specifically defines callbacks that respond to GitHub Copilot requests.
"""
