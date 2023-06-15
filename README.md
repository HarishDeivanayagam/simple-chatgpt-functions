# Simple ChatGPT Functions

This is a simple chatgpt functions framework. You can also look at example_foo.py

---

## How to use

Copy the framework.py

1. Create a class by inherting the ChatBot
```
class FooBot(ChatBot):
    def __init__(self):
        super().__init__(openai_api_key=os.getenv("OPENAI_API_KEY"), bot_description="foo bot")
```

2. @chatfunc decorator is used to notify its a chatbot function
   - Description tells the ChatGPT when to use the function
   - Args tells the ChatGPT about the description of the arguments 

```
@chatfunc(description="Foo Func", args=["pass an bar"])
def foo(self, bar):
    return f"""
    Func func call completed. Here is the output
    Hello {bar}
    """
```

3. Run your Bot!
```
foobot = FooBot()
response = foobot.chat("Call Foo with a World bar")
print(response)
```
