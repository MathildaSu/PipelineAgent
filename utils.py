def generate_prompt(prompt_filepath):
    with open(prompt_filepath, "r") as f:
        prompt_template = f.read()
        return prompt_template