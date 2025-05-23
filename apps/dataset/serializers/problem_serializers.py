# coding=utf-8
"""
@project: maxkb
@Author：虎
@file： problem_serializers.py
@date：2023/10/23 13:55
@desc:
"""

import os
import uuid
from functools import reduce
from typing import Dict, List

from django.db import transaction
from django.db.models import QuerySet
from drf_yasg import openapi
from rest_framework import serializers

from common.db.search import native_search, native_page_search
from common.mixins.api_mixin import ApiMixin
from common.util.field_message import ErrMessage
from common.util.file_util import get_file_content
from dataset.models import Problem, Paragraph, ProblemParagraphMapping, DataSet
from dataset.serializers.common_serializers import get_embedding_model_id_by_dataset_id
from embedding.models import SourceType
from embedding.task import (
    delete_embedding_by_source_ids,
    update_problem_embedding,
    embedding_by_data_list,
)
from smartdoc.conf import PROJECT_DIR
from django.utils.translation import gettext_lazy as _


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ["id", "content", "dataset_id", "create_time", "update_time"]


class ProblemInstanceSerializer(ApiMixin, serializers.Serializer):
    id = serializers.CharField(
        required=False, error_messages=ErrMessage.char(_("problem id"))
    )

    content = serializers.CharField(
        required=True, max_length=256, error_messages=ErrMessage.char(_("content"))
    )

    @staticmethod
    def get_request_body_api():
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["content"],
            properties={
                "id": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title=_("Issue ID is passed when modifying, not when creating."),
                ),
                "content": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title=_("content"),
                ),
            },
        )


class AssociationParagraph(serializers.Serializer):
    paragraph_id = serializers.UUIDField(
        required=True, error_messages=ErrMessage.uuid(_("paragraph id"))
    )
    document_id = serializers.UUIDField(
        required=True, error_messages=ErrMessage.uuid(_("document id"))
    )


class BatchAssociation(serializers.Serializer):
    problem_id_list = serializers.ListField(
        required=True,
        error_messages=ErrMessage.list(_("problem id list")),
        child=serializers.UUIDField(
            required=True, error_messages=ErrMessage.uuid(_("problem id"))
        ),
    )
    paragraph_list = AssociationParagraph(many=True)


def is_exits(exits_problem_paragraph_mapping_list, new_paragraph_mapping):
    filter_list = [
        exits_problem_paragraph_mapping
        for exits_problem_paragraph_mapping in exits_problem_paragraph_mapping_list
        if str(exits_problem_paragraph_mapping.paragraph_id)
        == new_paragraph_mapping.paragraph_id
        and str(exits_problem_paragraph_mapping.problem_id)
        == new_paragraph_mapping.problem_id
        and str(exits_problem_paragraph_mapping.dataset_id)
        == new_paragraph_mapping.dataset_id
    ]
    return len(filter_list) > 0


def to_problem_paragraph_mapping(
    problem, document_id: str, paragraph_id: str, dataset_id: str
):
    return ProblemParagraphMapping(
        id=uuid.uuid1(),
        document_id=document_id,
        paragraph_id=paragraph_id,
        dataset_id=dataset_id,
        problem_id=str(problem.id),
    ), problem


class ProblemSerializers(ApiMixin, serializers.Serializer):
    class Create(serializers.Serializer):
        dataset_id = serializers.UUIDField(
            required=True, error_messages=ErrMessage.uuid(_("dataset id"))
        )
        problem_list = serializers.ListField(
            required=True,
            error_messages=ErrMessage.list(_("problem list")),
            child=serializers.CharField(
                required=True,
                max_length=256,
                error_messages=ErrMessage.char(_("problem")),
            ),
        )

        def batch(self, with_valid=True):
            if with_valid:
                self.is_valid(raise_exception=True)
            problem_list = self.data.get("problem_list")
            problem_list = list(set(problem_list))
            dataset_id = self.data.get("dataset_id")
            exists_problem_content_list = [
                problem.content
                for problem in QuerySet(Problem).filter(
                    dataset_id=dataset_id, content__in=problem_list
                )
            ]
            problem_instance_list = [
                Problem(id=uuid.uuid1(), dataset_id=dataset_id, content=problem_content)
                for problem_content in problem_list
                if (
                    not exists_problem_content_list.__contains__(problem_content)
                    if len(exists_problem_content_list) > 0
                    else True
                )
            ]

            QuerySet(Problem).bulk_create(problem_instance_list) if len(
                problem_instance_list
            ) > 0 else None
            return [
                ProblemSerializer(problem_instance).data
                for problem_instance in problem_instance_list
            ]

    class Query(serializers.Serializer):
        dataset_id = serializers.UUIDField(
            required=True, error_messages=ErrMessage.uuid(_("dataset id"))
        )
        content = serializers.CharField(
            required=False, error_messages=ErrMessage.char(_("content"))
        )

        def get_query_set(self):
            query_set = QuerySet(model=Problem)
            query_set = query_set.filter(**{"dataset_id": self.data.get("dataset_id")})
            if "content" in self.data:
                query_set = query_set.filter(
                    **{"content__icontains": self.data.get("content")}
                )
            query_set = query_set.order_by("-create_time")
            return query_set

        def list(self):
            query_set = self.get_query_set()
            return native_search(
                query_set,
                select_string=get_file_content(
                    os.path.join(
                        PROJECT_DIR, "apps", "dataset", "sql", "list_problem.sql"
                    )
                ),
            )

        def page(self, current_page, page_size):
            query_set = self.get_query_set()
            return native_page_search(
                current_page,
                page_size,
                query_set,
                select_string=get_file_content(
                    os.path.join(
                        PROJECT_DIR, "apps", "dataset", "sql", "list_problem.sql"
                    )
                ),
            )

    class BatchOperate(serializers.Serializer):
        dataset_id = serializers.UUIDField(
            required=True, error_messages=ErrMessage.uuid(_("dataset id"))
        )

        def delete(self, problem_id_list: List, with_valid=True):
            if with_valid:
                self.is_valid(raise_exception=True)
            dataset_id = self.data.get("dataset_id")
            problem_paragraph_mapping_list = QuerySet(ProblemParagraphMapping).filter(
                dataset_id=dataset_id, problem_id__in=problem_id_list
            )
            source_ids = [row.id for row in problem_paragraph_mapping_list]
            problem_paragraph_mapping_list.delete()
            QuerySet(Problem).filter(id__in=problem_id_list).delete()
            delete_embedding_by_source_ids(source_ids)
            return True

        def association(self, instance: Dict, with_valid=True):
            if with_valid:
                self.is_valid(raise_exception=True)
                BatchAssociation(data=instance).is_valid(raise_exception=True)
            dataset_id = self.data.get("dataset_id")
            paragraph_list = instance.get("paragraph_list")
            problem_id_list = instance.get("problem_id_list")
            problem_list = QuerySet(Problem).filter(id__in=problem_id_list)
            exits_problem_paragraph_mapping = QuerySet(ProblemParagraphMapping).filter(
                problem_id__in=problem_id_list,
                paragraph_id__in=[p.get("paragraph_id") for p in paragraph_list],
            )
            problem_paragraph_mapping_list = [
                (problem_paragraph_mapping, problem)
                for problem_paragraph_mapping, problem in reduce(
                    lambda x, y: [*x, *y],
                    [
                        [
                            to_problem_paragraph_mapping(
                                problem,
                                paragraph.get("document_id"),
                                paragraph.get("paragraph_id"),
                                dataset_id,
                            )
                            for paragraph in paragraph_list
                        ]
                        for problem in problem_list
                    ],
                    [],
                )
                if not is_exits(
                    exits_problem_paragraph_mapping, problem_paragraph_mapping
                )
            ]
            QuerySet(ProblemParagraphMapping).bulk_create(
                [
                    problem_paragraph_mapping
                    for problem_paragraph_mapping, problem in problem_paragraph_mapping_list
                ]
            )
            data_list = [
                {
                    "text": problem.content,
                    "is_active": True,
                    "source_type": SourceType.PROBLEM,
                    "source_id": str(problem_paragraph_mapping.id),
                    "document_id": str(problem_paragraph_mapping.document_id),
                    "paragraph_id": str(problem_paragraph_mapping.paragraph_id),
                    "dataset_id": dataset_id,
                }
                for problem_paragraph_mapping, problem in problem_paragraph_mapping_list
            ]
            model_id = get_embedding_model_id_by_dataset_id(self.data.get("dataset_id"))
            embedding_by_data_list(data_list, model_id=model_id)

    class Operate(serializers.Serializer):
        dataset_id = serializers.UUIDField(
            required=True, error_messages=ErrMessage.uuid(_("dataset id"))
        )

        problem_id = serializers.UUIDField(
            required=True, error_messages=ErrMessage.uuid(_("problem id"))
        )

        def list_paragraph(self, with_valid=True):
            if with_valid:
                self.is_valid(raise_exception=True)
            problem_paragraph_mapping = QuerySet(ProblemParagraphMapping).filter(
                dataset_id=self.data.get("dataset_id"),
                problem_id=self.data.get("problem_id"),
            )
            if problem_paragraph_mapping is None or len(problem_paragraph_mapping) == 0:
                return []
            return native_search(
                QuerySet(Paragraph).filter(
                    id__in=[row.paragraph_id for row in problem_paragraph_mapping]
                ),
                select_string=get_file_content(
                    os.path.join(
                        PROJECT_DIR, "apps", "dataset", "sql", "list_paragraph.sql"
                    )
                ),
            )

        def one(self, with_valid=True):
            if with_valid:
                self.is_valid(raise_exception=True)
            return ProblemInstanceSerializer(
                QuerySet(Problem).get(**{"id": self.data.get("problem_id")})
            ).data

        @transaction.atomic
        def delete(self, with_valid=True):
            if with_valid:
                self.is_valid(raise_exception=True)
            problem_paragraph_mapping_list = QuerySet(ProblemParagraphMapping).filter(
                dataset_id=self.data.get("dataset_id"),
                problem_id=self.data.get("problem_id"),
            )
            source_ids = [row.id for row in problem_paragraph_mapping_list]
            problem_paragraph_mapping_list.delete()
            QuerySet(Problem).filter(id=self.data.get("problem_id")).delete()
            delete_embedding_by_source_ids(source_ids)
            return True

        @transaction.atomic
        def edit(self, instance: Dict, with_valid=True):
            if with_valid:
                self.is_valid(raise_exception=True)
            problem_id = self.data.get("problem_id")
            dataset_id = self.data.get("dataset_id")
            content = instance.get("content")
            problem = (
                QuerySet(Problem).filter(id=problem_id, dataset_id=dataset_id).first()
            )
            QuerySet(DataSet).filter(id=dataset_id)
            problem.content = content
            problem.save()
            model_id = get_embedding_model_id_by_dataset_id(dataset_id)
            update_problem_embedding(problem_id, content, model_id)
