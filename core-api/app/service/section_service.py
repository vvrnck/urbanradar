from app.serializer.section import SectionPost, SectionResponseList, SectionResponse
from app.model.Layer import Section
from ext import db
from typing import List


def create_section(section_model: SectionPost) -> Section:
    section = Section(**section_model.dict(by_alias=True))
    db.session.add(section)
    db.session.commit()
    return section


def list_sections(tenant_id) -> List[dict]:
    section_list = db.session.query(Section.id, Section.icon, Section.tenant, Section.name, Section.label).filter(Section.tenant == tenant_id).order_by(Section.order).all()
    section_resp = [SectionResponseList.from_orm(section).dict() for section in section_list]
    return section_resp


def get_section_by_id(section_id, tenant_id) -> Section:
    section_resp = db.session.query(Section).filter(Section.tenant == tenant_id).filter(Section.id == section_id).first()
    return section_resp


def delete_section_by_id(section_id: str, tenant_id: int) -> bool:
    db.session.query(Section).filter(Section.id == section_id).filter(Section.tenant == tenant_id).delete()
    db.session.commit()
    return True


def update_section_by_id(section_id: str, tenant_id: int, section_data: SectionPost) -> Section:
    section = get_section_by_id(section_id, tenant_id)
    sect_dict = section_data.dict(by_alias=True)
    for data in sect_dict.keys():
        section.__setattr__(data, sect_dict.get(data))
    db.session.commit()
    return section
