# -*- coding: utf-8 -*-
# Copyright (c) 2023 Sagi Shnaidman <sshnaidm@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: llm_analyzer
    type: notification
    short_description: Analyzes Ansible tasks and playbooks with various AI models
    description:
      - Analyzes Ansible tasks and playbooks using different AI providers
      - Validates API keys before playbook execution
      - Prints explanations for the tasks and playbooks
      - Saves explanations to markdown files in llm_analysis directory
      - Suggests improvements to the tasks and playbooks if any
      - Automatically disables if API key validation fails
    requirements:
      - enable in configuration - see examples section below for details
      - install required provider libraries (openai, google.generativeai, etc.)

    options:
      provider:
        description: AI provider to use
        choices: ['openai', 'gemini', 'groq', 'openrouter', 'cohere', 'anthropic']
        default: openai
        env:
          - name: AI_PROVIDER
        ini:
          - section: callback_llm_analyzer
            key: provider
      api_key:
        description: |
          API key for the chosen provider. Can be provided directly or via environment variables:
          - For OpenAI: OPENAI_API_KEY
          - For Gemini: GEMINI_API_KEY or GOOGLE_API_KEY
          - For Groq: GROQ_API_KEY
          - For OpenRouter: OPENROUTER_API_KEY
          - For Cohere: COHERE_API_KEY
          - For Anthropic: ANTHROPIC_API_KEY
          The API key must be set either through this option or the corresponding environment variable.
        env:
          - name: OPENAI_API_KEY
          - name: GEMINI_API_KEY
          - name: GROQ_API_KEY
          - name: OPENROUTER_API_KEY
          - name: COHERE_API_KEY
          - name: ANTHROPIC_API_KEY
        ini:
          - section: callback_llm_analyzer
            key: api_key
      model:
        description: Model to use for the chosen provider
        default: gpt-4
        env:
          - name: AI_MODEL
        ini:
          - section: callback_llm_analyzer
            key: model
      temperature:
        description: Temperature for AI response
        default: 0.4
        env:
          - name: AI_TEMPERATURE
        ini:
          - section: callback_llm_analyzer
            key: temperature
      max_tokens:
        description: Maximum tokens for AI response
        env:
          - name: AI_MAX_TOKENS
        ini:
          - section: callback_llm_analyzer
            key: max_tokens

    examples: |
      # Enable the callback plugin in ansible.cfg
      [defaults]
      callbacks_enabled = llm_analyzer

      # Configure the plugin in ansible.cfg
      [callback_llm_analyzer]
      provider = openai
      api_key = sk-xxx  # Or set via OPENAI_API_KEY environment variable
      model = gpt-4
      temperature = 0.4
      max_tokens = 1000

      # Example using environment variables with Gemini
      export AI_PROVIDER=gemini
      export GEMINI_API_KEY=your-key
      export AI_MODEL=gemini-1.5-pro
      ansible-playbook playbook.yml

      # Example using Groq
      [callback_llm_analyzer]
      provider = groq
      api_key = gsk-xxx  # Or set via GROQ_API_KEY environment variable
      model = llama-3.3-70b-versatile

      # Example using Cohere
      [callback_llm_analyzer]
      provider = cohere
      api_key = xxx  # Or set via COHERE_API_KEY environment variable
      model = command-r-plus-08-2024

      # Example using OpenRouter
      [callback_llm_analyzer]
      provider = openrouter
      api_key = sk-xxx  # Or set via OPENROUTER_API_KEY environment variable
      model = anthropic/claude-3-opus
"""

import datetime
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from ansible.module_utils._text import to_text
from ansible.plugins.callback import CallbackBase

# Provider-specific imports
AVAILABLE_PROVIDERS = {}

try:
    import openai
    from openai import OpenAI

    AVAILABLE_PROVIDERS["openai"] = True
except ImportError:
    AVAILABLE_PROVIDERS["openai"] = False

try:
    import google.generativeai as genai

    AVAILABLE_PROVIDERS["gemini"] = True
except ImportError:
    AVAILABLE_PROVIDERS["gemini"] = False

try:
    import groq

    AVAILABLE_PROVIDERS["groq"] = True
except ImportError:
    AVAILABLE_PROVIDERS["groq"] = False

try:
    import cohere

    AVAILABLE_PROVIDERS["cohere"] = True
except ImportError:
    AVAILABLE_PROVIDERS["cohere"] = False

try:
    import anthropic

    AVAILABLE_PROVIDERS["anthropic"] = True
except ImportError:
    AVAILABLE_PROVIDERS["anthropic"] = False

# OpenRouter uses OpenAI's client
AVAILABLE_PROVIDERS["openrouter"] = AVAILABLE_PROVIDERS["openai"]


class AIProvider:
    def __init__(
        self,
        provider: str,
        api_key: str,
        model: str,
        temperature: float,
        max_tokens: Optional[int],
    ):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None
        self.api_callers = {}  # Initialize api_callers here
        self._setup_client()

    def validate_api_key(self) -> bool:
        """Validate the API key for the chosen provider."""
        if not self.api_key:
            print(f"No API key provided for {self.provider}")
            return False

        if not AVAILABLE_PROVIDERS.get(self.provider):
            print(
                f"Provider {self.provider} is not available. Please install required library."
            )
            return False

        try:
            if self.provider in ["openai", "openrouter"]:
                # Test API key with a minimal request
                client = OpenAI(base_url="https://openrouter.ai/api/v1")
                client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=5,
                )
            elif self.provider == "gemini":
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel(self.model)
                model.generate_content("test")
            elif self.provider == "groq":
                client = groq.Groq(api_key=self.api_key)
                client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=5,
                )
            elif self.provider == "cohere":
                client = cohere.ClientV2(api_key=self.api_key)
                client.generate(
                    prompt="test", model=self.model, max_tokens=5
                )
            elif self.provider == "anthropic":
                client = anthropic.Anthropic(api_key=self.api_key)
                client.messages.create(
                    model=self.model,
                    max_tokens=5,
                    messages=[{"role": "user", "content": "test"}],
                )
            return True
        except Exception as e:
            print(f"API key validation failed for {self.provider}: {str(e)}")
            return False

    def _setup_client(self):
        if not self.api_key:
            raise ValueError(f"API key not provided for {self.provider}")

        if self.provider in ["openai", "openrouter"]:
            os.environ["OPENAI_API_KEY"] = self.api_key
            if self.provider == "openrouter":
                # TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url="https://openrouter.ai/api/v1")'
                self.client = OpenAI(base_url="https://openrouter.ai/api/v1")
            elif self.provider == "openai":
                self.client = OpenAI()
            self.api_callers["openai"] = self._call_openai_api
            self.api_callers["openrouter"] = self._call_openai_api
        elif self.provider == "gemini":
            os.environ["GOOGLE_API_KEY"] = self.api_key
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
            self.api_callers["gemini"] = self._call_gemini_api
        elif self.provider == "groq":
            os.environ["GROQ_API_KEY"] = self.api_key
            self.client = groq.Groq(api_key=self.api_key)
            self.api_callers["groq"] = self._call_groq_api
        elif self.provider == "cohere":
            os.environ["COHERE_API_KEY"] = self.api_key
            self.client = cohere.ClientV2(api_key=self.api_key)
            self.api_callers["cohere"] = self._call_cohere_api
        elif self.provider == "anthropic":
            os.environ["ANTHROPIC_API_KEY"] = self.api_key
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.api_callers["anthropic"] = self._call_anthropic_api

    def _create_prompt(
        self, task_text: Optional[str] = None, play_text: Optional[str] = None
    ) -> str:
        if task_text:
            return (
                "Review the following Ansible code: "
                f"\n```\n{task_text}```\n"
                "Analyze its function, adherence to best practices, potential issues, "
                "and inefficiencies. Then provide your response in this format:\n"
                "1. First explain the current code and any issues\n"
                "2. After 'IMPROVED CODE:', provide the complete improved version of the code\n"
                "3. After 'EXPLANATION:', explain your improvements\n\n"
                "Consider Ansible best practices and general programming principles (DRY, least astonishment)."
            )
        elif play_text:
            return (
                "Review the following Ansible playbook, "
                "focusing on overall purpose and effectiveness:"
                f"\n```\n{play_text}```\n"
                "Provide your response in this format:\n"
                "1. First explain the playbook's function\n"
                "2. After 'IMPROVED CODE:', provide the complete improved version of the playbook\n"
                "3. After 'EXPLANATION:', explain your improvements\n\n"
                "If no improvements are needed, write 'IMPROVED CODE: No improvements needed'"
            )
        return ""

    def _call_openai_api(self, prompt):
        kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant and Ansible expert.",
                },
                {"role": "user", "content": prompt},
            ],
        }
        if self.temperature is not None:
            kwargs["temperature"] = self.temperature
        if self.max_tokens:
            kwargs["max_tokens"] = self.max_tokens

        # Add OpenRouter specific headers if using OpenRouter
        if self.provider == "openrouter":
            kwargs["extra_headers"] = {
                "HTTP-Referer": "https://github.com/ansible/ansible",  # Identifies your application
                "X-Title": "Ansible LLM Analyzer",  # Name of your application
            }

        response = self.client.chat.completions.create(**kwargs)
        return to_text(response.choices[0].message.content.strip())

    def _call_gemini_api(self, prompt):
        response = self.client.generate_content(prompt)
        return to_text(response.text.strip())

    def _call_groq_api(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant and Ansible expert.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature if self.temperature is not None else 0.4,
            max_tokens=self.max_tokens if self.max_tokens else None,
        )
        return to_text(completion.choices[0].message.content.strip())

    def _call_cohere_api(self, prompt):
        response = self.client.generate(
            prompt=prompt,
            model=self.model,
            temperature=self.temperature if self.temperature is not None else 0.4,
            max_tokens=self.max_tokens if self.max_tokens else None,
        )
        return to_text(response.generations[0].text.strip())

    def _call_anthropic_api(self, prompt):
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens if self.max_tokens else 1024,
            temperature=self.temperature if self.temperature is not None else 0.4,
            system="You are a helpful assistant and Ansible expert.",
            messages=[{"role": "user", "content": prompt}],
        )
        return to_text(message.content[0].text.strip())

    def get_description(
        self, task_text: Optional[str] = None, play_text: Optional[str] = None
    ) -> str:
        if not AVAILABLE_PROVIDERS.get(self.provider):
            return to_text(f"Please install the required library for {self.provider}")

        if not self.api_key:
            return to_text(f"Please set the API key for {self.provider}")

        prompt = self._create_prompt(task_text, play_text)

        try:
            api_caller = self.api_callers.get(self.provider)
            if api_caller:
                return api_caller(prompt)
            else:
                return to_text("Unsupported provider")

        except Exception as e:
            return to_text(f"Error with {self.provider}: {str(e)}")


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 1.1
    CALLBACK_TYPE = "aggregate"
    CALLBACK_NAME = "llm_analyzer"
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.ai_provider = None
        self.analysis_dir = Path("llm_analysis")
        self.analysis_dir.mkdir(exist_ok=True)
        self.task_count = 0
        self.play_count = 0

    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(CallbackModule, self).set_options(
            task_keys=task_keys, var_options=var_options, direct=direct
        )

        provider = self.get_option("provider")
        # Try to get provider-specific API key from environment first
        api_key = os.getenv(f"{provider.upper()}_API_KEY")

        # If not found in environment, try the generic api_key from ansible.cfg
        if not api_key:
            api_key = self.get_option("api_key")

        try:
            self.ai_provider = AIProvider(
                provider=provider,
                api_key=api_key,
                model=self.get_option("model"),
                temperature=float(self.get_option("temperature")),
                max_tokens=self.get_option("max_tokens"),
            )
        except Exception as e:
            self.disabled = True
            print(
                f"\nLLM Analyzer disabled: Failed to initialize provider {provider}: {str(e)}"
            )
            return

        # Validate API key before proceeding
        if not self.ai_provider.validate_api_key():
            self.disabled = True
            print(f"\nLLM Analyzer disabled: Invalid API key for {provider}")
            return

    def _extract_improvements(self, content: str) -> Dict[str, Any]:
        """Extract improved code and explanation from the AI response."""
        result = {"improved_code": None, "explanation": None, "has_improvements": False}

        # Split content at "IMPROVED CODE:" marker
        parts = content.split("IMPROVED CODE:")
        if len(parts) < 2:
            return result

        improved_section = parts[1].strip()

        # Check if no improvements needed
        if improved_section.lower().startswith("no improvements needed"):
            return result

        # Split at "EXPLANATION:" to separate code and explanation
        code_parts = improved_section.split("EXPLANATION:")
        if len(code_parts) < 2:
            result["improved_code"] = improved_section.strip()
        else:
            result["improved_code"] = code_parts[0].strip()
            result["explanation"] = code_parts[1].strip()

        result["has_improvements"] = bool(result["improved_code"])
        return result

    def _save_to_yaml(
        self, improvements: Dict[str, Any], analysis_type: str, name: str = None
    ):
        """Save improvements to a YAML file."""
        if not improvements["has_improvements"]:
            return

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        count = self.task_count if analysis_type == "task" else self.play_count
        filename = f"{timestamp}_{analysis_type}_{count}"
        if name:
            # Replace spaces and special characters with underscores
            safe_name = "".join(c if c.isalnum() else "_" for c in name)
            filename = f"{filename}_{safe_name}"
        filename = f"{filename}_improved.yml"

        filepath = self.analysis_dir / filename
        data = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": analysis_type,
            "name": name if name else f"{analysis_type}_{count}",
            "improved_code": improvements["improved_code"],
            "explanation": improvements["explanation"],
        }

        with open(filepath, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def _save_to_markdown(self, content: str, analysis_type: str, name: str = None):
        """Save analysis to a markdown file."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        count = self.task_count if analysis_type == "task" else self.play_count
        filename = f"{timestamp}_{analysis_type}_{count}"
        if name:
            # Replace spaces and special characters with underscores
            safe_name = "".join(c if c.isalnum() else "_" for c in name)
            filename = f"{filename}_{safe_name}"
        filename = f"{filename}.md"

        filepath = self.analysis_dir / filename
        with open(filepath, "w") as f:
            f.write(f"# {analysis_type.title()} Analysis\n\n")
            if name:
                f.write(f"**Name:** {name}\n\n")
            f.write(
                f"**Timestamp:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write("## Analysis\n\n")
            f.write(content)

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.task_count += 1
        task_text = yaml.dump([json.loads(json.dumps(task._ds))])
        explanation = self.ai_provider.get_description(task_text=task_text)

        # Print to console
        print(f"Explanation: \n{explanation}")

        # Extract improvements and save to YAML if any exist
        improvements = self._extract_improvements(explanation)
        if improvements["has_improvements"]:
            self._save_to_yaml(improvements, "task", task.get_name())

        # Save full analysis to markdown
        self._save_to_markdown(explanation, "task", task.get_name())

    def v2_playbook_on_play_start(self, play):
        self.play_count += 1
        play_text = yaml.dump(json.loads(json.dumps(play.get_ds())))
        explanation = self.ai_provider.get_description(play_text=play_text)

        # Print to console
        print(f"Explanation: \n{explanation}")

        # Extract improvements and save to YAML if any exist
        improvements = self._extract_improvements(explanation)
        if improvements["has_improvements"]:
            self._save_to_yaml(improvements, "play", play.get_name())

        # Save full analysis to markdown
        self._save_to_markdown(explanation, "play", play.get_name())
