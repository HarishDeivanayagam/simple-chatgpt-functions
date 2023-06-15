from .framework import ChatBot, chatfunc
import os

class FooBot(ChatBot):
    def __init__(self):
        super().__init__(openai_api_key=os.getenv("OPENAI_API_KEY"), bot_description="foo bot")


    @chatfunc(description="Foo Func", args=["pass an bar"])
    def foo(self, bar):
        return f"""
        Func func call completed. Here is the output
        Hello {bar}
        """


foobot = FooBot()
response = foobot.chat("Call Foo with a World bar")
print(response)
