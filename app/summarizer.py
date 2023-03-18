import openai
import tiktoken
from os import getenv

class Summarizer():
    prompt = None

    def __init__(self, token=None, prompt=None):
        if token:
            openai.api_key = token
        else:
            openai.api_key = getenv("OPENAI_API_KEY")

        if prompt:
            self.prompt = prompt

    def num_tokens_from_string(self, string: str, encoding_name: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def transcription_summarize(self, text, format="markdown"):
        print("transcription_summarize")
        gpt3Encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        num_tokens = self.num_tokens_from_string(text, gpt3Encoding.name)
        chunk = 4096 - 512

        if num_tokens < chunk:
            return self.summarize_in_one_chunk(text, format)
        else:
            return "Transcription is too long"
            # return self.summarize_big_chunks(text, chunk)

    def summarize_in_one_chunk(self, text, format):
        messages = [
            {"role": "system", "content": self.generate_prompt(format)},
        ]
        messages.append({"role": "user", "content": text})
        print("ChatCompletion short")
        response = ""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0,
                n=1,
                presence_penalty=2,
                frequency_penalty=2,
                max_tokens=512,
            )
        except Exception as e:
            print(e)
            return "Error"

        print(response)

        return response['choices'][0]['message']['content']

    def generate_prompt(self, format="markdown"):
        if self.prompt:
            return self.prompt

        prompt = """ 
    You are specialist in summarizing textual information provided to you. 
    You need to summarize  transcribed text that is extracted from a youtube video to keypoints only.
    Skip all the unnecessary information, adverisements, sponsored parts, etc.
    Do it in less than 1000 chars max.

    Expected response: 
    Key Points: 
    * [Key Point short and concise]
    ...
    """

        if format == "markdown":
            prompt += """
            Format response as markdown."""

        else:
            prompt += """
            Format response as valid html. Wrap key points in <ul> and <li> tags."""

        prompt += """
        User provides the input"""

        return prompt


class MockSummarizer():
    def __init__(self, token=None, prompt=None):
        super().__init__(token, prompt)

    def summarize_in_one_chunk(self, text, format):
        return "This is a summary"

    def summarize_big_chunks(self, text, chunk):
        return "This is a summary"

    def generate_prompt(self, format="markdown"):
        return "This is a prompt"

    def transcription_summarize(self, text, format="markdown"):
        return """ <p>Key Points:</p>
<ul>
<li>* Use Google Ads Keyword Planner to find a trending keyword</li>
<li>* Prompt Chat GPT with the chosen keyword and ask it to understand your brand's information</li>
<li>* Add bullet points, headings, and internal links using an app script in Google Sheets</li>
<li>* The content generated by Chat GPT will be unique as it includes input from your brand </li></ul>"""
