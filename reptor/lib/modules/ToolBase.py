import sys
import logging

from xml.etree import ElementTree

from reptor.api.NotesAPI import NotesAPI

from .Base import Base

log = logging.getLogger("reptor")


class ToolBase(Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = kwargs.get("action")
        self.note_icon = "🛠️"
        self.raw_input = None
        self.parsed_input = None
        self.formatted_input = None
        self.no_timestamp = self.config.get("cli", dict()).get("no_timestamp")
        self.force_unlock = self.config.get("cli", dict()).get("force_unlock")

        self.input_format = kwargs.get("format")

    @classmethod
    def add_arguments(cls, parser):
        super().add_arguments(parser)
        action_group = parser.add_mutually_exclusive_group()
        action_group.title = 'action_group'
        action_group.add_argument(
            "-parse", "--parse", action='store_const', dest='action', const='parse', default='format',
        )
        action_group.add_argument(
            "-format", "--format", action='store_const', dest='action', const='format', default='format',
        )
        action_group.add_argument(
            "-upload", "--upload", action='store_const', dest='action', const='upload', default='format',
        )

        input_format_group = parser.add_mutually_exclusive_group()
        input_format_group.title = 'input_format_group'
        # Add parsing options only if implemented by modules
        if cls.parse_xml != ToolBase.parse_xml:
            input_format_group.add_argument(
                "-xml", "--xml", action='store_const', dest='format', const='xml', default='raw',
            )
        if cls.parse_json != ToolBase.parse_json:
            input_format_group.add_argument(
                "-json", "--json", action='store_const', dest='format', const='json', default='raw',
            )
        if cls.parse_csv != ToolBase.parse_csv:
            input_format_group.add_argument(
                "-csv", "--csv", action='store_const', dest='format', const='csv', default='raw',
            )

    def run(self):
        if self.action == "parse":
            self.parse()
            self.reptor.logger.display(self.parsed_input)
        elif self.action == "format":
            self.format()
            self.reptor.logger.display(self.formatted_input)
        elif self.action == "upload":
            self.upload()

    def load(self):
        self.raw_input = sys.stdin.read()

    def parse_xml(self):
        raise NotImplementedError(
            'Parse xml data is not implemented for this plugin.')

    def parse_json(self):
        raise NotImplementedError(
            'Parse json data is not implemented for this plugin.')

    def parse_csv(self):
        raise NotImplementedError(
            'Parse csv data is not implemented for this plugin.')

    def parse_raw(self):
        raise NotImplementedError(
            'Parse raw data is not implemented for this plugin.')

    def parse(self):
        if not self.raw_input and not self.file_path:
            self.load()

        if self.input_format == "xml":
            if not self.file_path and self.raw_input:
                self.xml_root = ElementTree.fromstring(self.raw_input)
            else:
                self.xml_root = ElementTree.parse(self.file_path).getroot()
            self.parse_xml()
        elif self.input_format == "json":
            self.parse_json()
        elif self.input_format == "csv":
            self.parse_csv()

    def format(self):
        if not self.parsed_input:
            self.parse()

    def upload(self):
        if not self.formatted_input:
            self.format()
        notename = self.notename or self.__class__.__name__.lower()
        parent_notename = "Uploads" if notename != "Uploads" else None

        NotesAPI(self.reptor).write_note(
            notename=notename,
            parent_notename=parent_notename,
            content=self.formatted_input,
            icon=self.note_icon,
            no_timestamp=self.no_timestamp,
            force_unlock=self.force_unlock,
        )
