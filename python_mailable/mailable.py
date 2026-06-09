from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Self

from jinja2 import Environment, FileSystemLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Mailable(ABC):
    _to_email: Optional[str] = None
    _to_cc: list[str] = field(default_factory=list)
    _to_bcc: list[str] = field(default_factory=list)

    _subject_line: str = ""
    _template_path: str = ""

    _text_template_path: str = ""

    _context: dict[str, Any] = field(default_factory=dict)
    _attachments: list[str] = field(default_factory=list)

    def to(self, recipient_email: str) -> Self:
        self._to_email = recipient_email
        return self

    def cc(self, *emails: str) -> Self:
        self._to_cc.extend(emails)
        return self

    def bcc(self, *emails: str) -> Self:
        self._to_bcc.extend(emails)
        return self

    def subject(self, subject_line: str) -> Self:
        self._subject_line = subject_line
        return self

    def template(self, path: str) -> Self:
        self._template_path = path
        return self

    def text_template(self, path: str) -> Self:
        self._text_template_path = path
        return self

    def with_context(self, context_dict: dict[str, Any]) -> Self:
        self._context.update(context_dict)
        return self

    def attach(self, file_path: str) -> Self:
        self._attachments.append(file_path)
        return self

    @abstractmethod
    def build(self) -> Self:
        """Subclasses define how the email is built."""
        pass

    def render(self, project_root: Path = PROJECT_ROOT, as_text: bool = False) -> Optional[str]:
        template_path = self._text_template_path if as_text else self._template_path

        if not template_path:
            return None

        environment = Environment(
            loader=FileSystemLoader(project_root),
            autoescape=True,
        )

        template = environment.get_template(template_path)

        return template.render(**self._context)

    def render_as_text(self, project_root: Path = PROJECT_ROOT) -> Optional[str]:
        return self.render(project_root, as_text=True)
