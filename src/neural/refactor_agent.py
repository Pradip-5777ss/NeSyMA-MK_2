import re
from typing import Optional
from .llm_provider import BaseLLMProvider
from .prompts import SYSTEM_PROMPT

class NeuralRefactorer:
    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider

    def clean_output(self, raw_text: str) -> str:
        # If the LLM disobeys and wraps output in markdown, strip it
        pattern = r"```python\n(.*?)\n```"
        match = re.search(pattern, raw_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # Also check for just ``` 
        pattern2 = r"```\n(.*?)\n```"
        match2 = re.search(pattern2, raw_text, re.DOTALL)
        if match2:
            return match2.group(1).strip()
            
        return raw_text.strip()

    def refactor(self, legacy_code: str, previous_errors: Optional[str] = None) -> str:
        prompt = f"{SYSTEM_PROMPT}\n\nLegacy Code:\n{legacy_code}"
        if previous_errors:
            prompt += f"\n\nYour previous attempt failed verification with this Z3 Error:\n{previous_errors}\nFix the mathematical logic and try again."
            
        raw_output = self.provider.generate_code(prompt)
        return self.clean_output(raw_output)
