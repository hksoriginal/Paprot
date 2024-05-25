import re

from Firewall.constants import MALICIOUS_STRINGS


class SecurityFirewall:
    def detect_string(self, text: str, prompt_text: str) -> bool:
        return text in prompt_text

    def check_malicious_string(self, prompt_text: str) -> bool:
        match_exists = []
        for match in MALICIOUS_STRINGS:
            match_exists.append(self.detect_string(match, prompt_text.lower()))
        return any(match_exists)

    def check_malicious_code_input(self, prompt_text: str) -> bool:
        pattern = r"```[a-zA-Z]+\n"
        matches = re.findall(pattern, prompt_text)
        if matches:
            print("\033[91mCode Injection Detected!!\033[0m")
            return True
        else:
            return False
