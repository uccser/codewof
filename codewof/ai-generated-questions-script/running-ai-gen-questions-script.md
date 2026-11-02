
You will need to have an openrouter account with funds attached, It cost just less $2 to run (as of october 2026). 


To run the ai_gen_questions script create a .env file in the same structure and location as .env.example

In the terminal navigate to ai-generated-questions-script then run the following commands. 

``python3 -m venv .venv``
``source .venv/bin/activate``
``pip install python-dotenv requests``
``python ai_gen_questions_script.py``



The vm is required so that the python package, dotenv, for reading the .env file, can be installed. 
You can avoid this and run the script directly if you replace this segmant :

```import dotenv

dotenv.load_dotenv()  # loads OPENROUTER_API_KEY from a .env file in this directory

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY not found - check your .env file has it set."
    )    
```
You can instead past your API key in here directly, 
