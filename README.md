# learn-ai-functions

This Azure Functions application provides two endpoints:

### {{url}}/api/GetSummary
- GetSummary recieves a POST request with a JSON body with two fields: "text", representing the text to summarize, and "sentences", representing the length of the output summary by the number of sentences.
- Example: { "text": "Hello World!", "sentences": 1 }
### {{url}}/api/GetInsights
- GetInsights recieves a POST request with a JSON body with one field: "text", representing the text to extract keywords from.
- This can *easily* be expanded to all other Azure Text Analytics APIs with minimal code changes. All you need to do is change up the URL and you're good to go.

## How to run
Insert your Text Analytics primary key into the GetInsights function, and follow the link:
https://docs.microsoft.com/en-us/azure/azure-functions/functions-develop-local

## TODO:
Create a proper key store for private keys
