import typing
from abc import abstractmethod

from .api.notes import ApiNotesProtocol
from .api.projects import ApiProjectsProtocol
from .api.templates import ApiTemplatesProtocol
from .api.project_designs import ApiProjectDesignsProtocol


class APIManagerProtocol(typing.Protocol):
    notes: ApiNotesProtocol
    projects: ApiProjectsProtocol
    project_desings: ApiProjectDesignsProtocol
    templates: ApiTemplatesProtocol
