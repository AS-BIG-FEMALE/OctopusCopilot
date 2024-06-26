from functools import reduce

from infrastructure.http_pool import http

max_docs_results = 5


def get_docs_context(search_results):
    if not search_results or "items" not in search_results or not isinstance(search_results["items"], list):
        return ""

    return reduce(lambda text, result: (text
                                        + http.request("GET",
                                                       result["html_url"]
                                                       .replace("/blob/", "/raw/"))
                                        .data.decode("utf-8")
                                        + "\n\n"),
                  search_results["items"][:max_docs_results], "")
