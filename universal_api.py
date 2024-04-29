import logging
import os
from openai import OpenAI

class UniversalAPI:
    def __init__(self):
        self.cached_methods = {}
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def __getattr__(self, name):
        def method(*args, **kwargs):
            method_signature = (name, len(args), tuple(sorted(kwargs.keys())))
            if method_signature in self.cached_methods:
                cached_method = self.cached_methods[method_signature]
                logging.info(f"Using cached method: {name} with arguments {args} and kwargs {kwargs}")
                return cached_method(*args, **kwargs)

            prompt = f"The user is asking for a method called {name} with arguments {args} and kwargs {kwargs}. Return the python code that implements this method. Only return the python code, without the ```python prefix and ``` sufix. Do not include example usage."
            messages = [
                {"role": "user", "content": prompt},
            ]
            logging.info(f"Generating dynamic method called: {name}, with arguments {args} and kwargs {kwargs}")
            response = self.openai_client.chat.completions.create(
                model='gpt-4-turbo-preview',
                messages=messages,
                max_tokens=256, # Adjust the number of tokens as needed
                temperature=0,  # Adjust the creativity level
            )
            llm_response = response.choices[0].message.content
            logging.info(f"LLM response: {llm_response}")
            exec(llm_response)
            self.cached_methods[method_signature] = locals()[name]
            return locals()[name](*args, **kwargs)

        return method

# Illustration
api = UniversalAPI()
print(api.sort([3, 2, 1])) # returns [1, 2, 3]
print(api.sort([4, 3, 2, 1])) # returns [1, 2, 3, 4] using cached implementation
print(api.sort([1, 2, 3], reverse=True)) # returns [3, 2, 1]
print(api.add(1, 2)) # returns 3
print(api.reverse('hello')) # returns 'olleh'
api.fizzbuzz(15) # prints the fizzbuzz sequence up to 15
api.print_picachu() # prints an ASCII art of Picachu
