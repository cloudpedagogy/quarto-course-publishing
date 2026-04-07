import pytest
from course_generator.core.config_loader import ConfigLoader
from course_generator.models.schema import CourseConfig, Module, Session, Section, Page

def test_config_validation():
    data = {
        "module": {
            "code": "TEST101",
            "title": "Test Module",
            "description": "A test module"
        },
        "sessions": [
            {
                "code": "S1",
                "title": "Session 1",
                "overview": "Overview",
                "sections": [
                    {
                        "number": 1,
                        "title": "Section 1",
                        "kind": "overview",
                        "pages": [
                            {"title": "Page 1", "kind": "text_page"}
                        ]
                    }
                ]
            }
        ]
    }
    config = CourseConfig(**data)
    assert config.module.code == "TEST101"
    assert len(config.sessions) == 1
    assert config.sessions[0].sections[0].number == 1
    assert config.sessions[0].sections[0].pages[0].title == "Page 1"
