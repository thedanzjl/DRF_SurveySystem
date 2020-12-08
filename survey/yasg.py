from collections import OrderedDict
from pathlib import Path

from django.conf import settings
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import no_body


class ReadOnly:
    def get_fields(self):
        new_fields = OrderedDict()
        for fieldName, field in super().get_fields().items():
            if not field.write_only:
                new_fields[fieldName] = field
        return new_fields


class WriteOnly:
    def get_fields(self):
        new_fields = OrderedDict()
        for fieldName, field in super().get_fields().items():
            if not field.read_only:
                new_fields[fieldName] = field
        return new_fields


class BlankMeta:
    pass


class ReadWriteAutoSchema(SwaggerAutoSchema):
    def get_view_serializer(self):
        return self._convert_serializer(WriteOnly)

    def get_default_response_serializer(self):
        body_override = self._get_request_body_override()
        if body_override and body_override is not no_body:
            return body_override

        return self._convert_serializer(ReadOnly)

    def _convert_serializer(self, new_class):
        serializer = super().get_view_serializer()
        if not serializer:
            return serializer

        class CustomSerializer(new_class, serializer.__class__):
            class Meta(getattr(serializer.__class__, "Meta", BlankMeta)):
                ref_name = new_class.__name__ + serializer.__class__.__name__

        new_serializer = CustomSerializer(data=serializer.data)
        return new_serializer


class SurveySchemaGenerator(OpenAPISchemaGenerator):
    """
    Задает базовый путь для API
    """

    def get_schema(self, request=None, public=False):
        schema = super(SurveySchemaGenerator, self).get_schema(request, public)
        schema.base_path = ""
        return schema


def generate_api_description():
    # keyword = "<API MODEL DESCRIPTION AUTO INSERTED HERE>"
    #
    # from core import models
    #
    # model_names = (model_name for model_name in dir(models) if model_name[0].isupper())
    #
    # lines = []
    # for model_name in model_names:
    #     model_class = getattr(models, model_name)
    #     docstring = model_class.__doc__
    #     if docstring and not docstring.startswith("\n"):
    #         docstring = f"\n  {docstring}\n"
    #     lines.append(f"* {model_class.__name__}:\n  {docstring}")

    with open(Path(settings.BASE_DIR) / "docs" / "description.md") as f:
        description = f.read()

    # description = description.replace(keyword, "\n".join(lines))
    return description
