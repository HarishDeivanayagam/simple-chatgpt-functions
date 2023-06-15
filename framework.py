import openai

def chatfunc(description: str, args: str):
    def decorator(func):
        func.description = description
        func.args = args

        return func

    return decorator

class ChatBot():

    def __init__(self, openai_api_key, bot_description, max_chats=100):
        self.chat_count = 0
        openai.api_key = openai_api_key
        self.max_chats = max_chats
        self.function_descriptions = []
        self.extract_function_descriptions()
        self.messages = [{
            "role": "system",
            "content": bot_description
        }]


    def chat(self, message, name=None, role="user"):
        if self.chat_count >= self.max_chats:
            return "too many requests"

        # your chat message
        if name is not None:
            self.messages.append({
                "name": name,
                "role": role,
                "content": message
            })

        else:
            self.messages.append({
                "role": role,
                "content": message
            })


        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=self.messages,
            functions=self.function_descriptions
        )

        response = response["choices"][0]["message"]

        self.chat_count += 1
        
        # If the ChatGPT responds with a function 
        if "function_call" in response:

            # Get the function name and arguments
            func_name=response["function_call"]["name"]
            func_args=eval(response["function_call"]["arguments"])

            call_func = getattr(self, func_name)

            data = call_func(**func_args)

            return self.chat(
                message=data, 
                name=func_name, 
                role="function"
            )

        # If the ChatGPT responds with content it will return content
        if "content" in response:
            return response["content"]


    # This function is used to declare the function schema for chatgpt functions
    def extract_function_descriptions(self):
        for _, attr_value in self.__class__.__dict__.items():
            if callable(attr_value) and hasattr(attr_value, "description") and hasattr(attr_value, "args"):

                function_args = list(attr_value.__code__.co_varnames)[1:][:attr_value.__code__.co_argcount - 1]

                function_description = {
                    "name": attr_value.__name__,
                    "description": attr_value.description,
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    },
                    "required": function_args
                }

                for i in range(0, len(function_args)):
                    
                    args_split = attr_value.args[i].split("::")

                    function_description["parameters"]["properties"][function_args[i]] = {
                        "type": args_split[1] if len(args_split) > 1 else "string",
                        "description": args_split[0]
                    }

                self.function_descriptions.append(function_description)
