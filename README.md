# universal-api

* Don't know how to implement a function? Let Universal API help you on the fly! *

This is a non-serious library that can implement any functions on the fly using LLMs. Generated functions are cached so you don't pay for things that are already implemented.

## Usage

```python
api = UniversalAPI()
print(api.sort([3, 2, 1])) # returns [1, 2, 3]
print(api.sort([3, 2, 1], reverse=True)) # returns [3, 2, 1]
print(api.add(1, 2)) # returns 3
print(api.reverse('hello')) # returns 'olleh'
```

## Warning
This library will execute external code in your local machine. It's NOT safe to run in production (or really, any serious environment).

## Notes
By default this library uses OpenAI API. You can modify environment variables like `OPENAI_BASE_URL` to use other LLM endpoints (e.g. Anyscale Endpoint), which allows you to run on other models like the LLama series.