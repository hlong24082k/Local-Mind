import asyncio

from src.llm.post_processor import PostProcessor
from src.llm.gemini_provider import GeminiProvider
from src.prompt.prompt_templates import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


async def main():
    gemini = GeminiProvider(model_name="gemini-2.5-flash")
    post_processor = PostProcessor()

    query = "Delete the all file with suffix image format"

    user_prompt = USER_PROMPT_TEMPLATE.format(user_input=query)
    system_prompt = SYSTEM_PROMPT

    prompt = f"{system_prompt}\n\n{user_prompt}"

    response = []

    async for chunk in gemini.generate(prompt):
        print(chunk, end="", flush=True)
        response.append(chunk)

    llm_output = "".join(response)

    result = post_processor.process(llm_output, return_json=True)
    print("[debug] final result: \n", result)

if __name__ == "__main__":
    asyncio.run(main())
