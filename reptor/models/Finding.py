import typing

from reptor.models.ProjectDesign import ProjectDesign
from reptor.models.Section import (
    SectionData,
    SectionDataField,
    SectionDataRaw,
    SectionRaw,
)


class FindingDataRaw(SectionDataRaw):
    """
    Custom finding fields will be added as additional attributes.

    Attributes:
        title:
        cvss:
        summary:
        description:
        precondition:
        impact:
        recommendation:
        short_recommendation:
        references:
        affected_components:
        owasp_top10_2021:
        wstg_category:
        retest_notes:
        retest_status:
        severity:
    """

    title: str = ""
    cvss: str = ""
    summary: str = ""
    description: str = ""
    precondition: str = ""
    impact: str = ""
    recommendation: str = ""
    short_recommendation: str = ""
    references: typing.List[str] = []
    affected_components: typing.List[str] = []
    owasp_top10_2021: str = ""
    wstg_category: str = ""
    retest_notes: str = ""
    retest_status: str = ""
    severity: str = ""


class FindingDataField(SectionDataField):
    ...


class FindingData(SectionData):
    title: FindingDataField
    cvss: FindingDataField
    summary: FindingDataField
    description: FindingDataField
    precondition: FindingDataField
    impact: FindingDataField
    recommendation: FindingDataField
    short_recommendation: FindingDataField
    references: FindingDataField
    affected_components: FindingDataField
    owasp_top10_2021: FindingDataField
    wstg_category: FindingDataField
    retest_notes: FindingDataField
    retest_status: FindingDataField
    severity: FindingDataField

    field_class = FindingDataField


class FindingRaw(SectionRaw):
    data: FindingDataRaw


class Finding(FindingRaw):
    data: FindingData

    def __init__(
        self,
        raw: typing.Union[FindingRaw, typing.Dict],
        project_design: typing.Optional[ProjectDesign] = None,
        force_compatible: bool = True,
    ):
        if project_design is None:
            project_design = ProjectDesign()
        if isinstance(raw, dict):
            raw = FindingRaw(raw)

        # Set attributes from FindingRaw
        for attr in typing.get_type_hints(FindingRaw).items():
            self.__setattr__(attr[0], raw.__getattribute__(attr[0]))
        self.data = FindingData(
            project_design.finding_fields, raw.data, force_compatible=force_compatible
        )

    @classmethod
    def from_translation(
        cls,
        translation: typing.Any,  # translation = FindingTemplateTranslation
        **kwargs,
    ):
        raw = FindingRaw(
            {"language": translation.language, "data": translation.data.to_dict()}
        )
        return cls(raw, **kwargs)
