import logging
import os
from openai import OpenAI

class UniversalAPI:
    def __init__(self):
        self.cached_methods = {}
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def __getattr__(self, name):
        if name in self.cached_methods:
            return self.cached_methods[name]
        def method(*args, **kwargs):
            prompt = "The user is asking for a method called " + name + " with arguments " + str(args) + " and kwargs " + str(kwargs) + ". Return the python code that implements this method. Only return the python code, without the ```python prefix and ``` sufix."
            messages = [
                {"role": "user", "content": prompt},
            ]
            logging.info(f"Dynamic method called: {name}, with arguments {args} and kwargs {kwargs}")
            response = self.openai_client.chat.completions.create(
                model='gpt-4-turbo-preview',
                messages=messages,
                max_tokens=256,  # Adjust the number of tokens as needed
                temperature=0,  # Adjust the creativity level
            )
            print(response.choices[0].message.content)
            exec(response.choices[0].message.content)
            print(*args, **kwargs)
            return locals()[name](*args, **kwargs)

        self.cached_methods[name] = method
        return method

# Illustration
api = UniversalAPI()
print(api.sort([3, 2, 1]))
