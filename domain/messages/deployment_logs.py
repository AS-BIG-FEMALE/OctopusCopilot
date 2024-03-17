def build_plain_text_prompt():
    """
    Build a message prompt for the LLM that instructs it to parse plain text
    :return: The messages to pass to the llm.
    """
    messages = [
        ("system", "You understand Octopus Deploy log files. "
         + "You are a concise and helpful agent. "
         + "Answer the question given the supplied text. You must assume that the supplied text relates to the project and environment in the question."),
        ("user", "{input}"),
        # https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api
        # Put instructions at the beginning of the prompt and use ### or """ to separate the instruction and context
        ("user", "Text: ###\n{context}\n###")]

    return messages