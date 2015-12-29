# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from ..models import ProgramType, ProgramArgumentField, ProgramArgument
from ..models.types_ import TYPES_FOR_DJANGO_FIELDS, DJANGO_FIELDS_FOR_TYPES

class ProgramTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramType


class ProgramArgumentFieldSerializer(serializers.ModelSerializer):
    schema = serializers.SerializerMethodField()

    class Meta:
        model = ProgramArgumentField
        exclude = ('program_argument', 'id')

    def get_schema(self, obj):
        schema = {}
        argument = obj.program_argument
        model = argument.content_type.model_class()
        field_name = obj.name
        field = model._meta.get_field(field_name)
        schema['data_type'] = TYPES_FOR_DJANGO_FIELDS[field.__class__]

        if field.__class__ in DJANGO_FIELDS_FOR_TYPES['model']:
            related_model_content_type = ContentType.objects.get_for_model(field.related_model)
            model = '{}.{}'.format(related_model_content_type.app_label, related_model_content_type.model_class().__name__)
            schema['model'] = model

        schema['verbose_name'] = field.verbose_name

        return schema

class ProgramArgumentSerializer(serializers.ModelSerializer):
    field = ProgramArgumentFieldSerializer(many=True)

    class Meta:
        model = ProgramArgument


class ProgramTypeSerializer(serializers.ModelSerializer):
    argument = ProgramArgumentSerializer(many=True)

    class Meta:
        model = ProgramType
