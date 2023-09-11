# Python imports
import uuid

# Django imports
from django.db.models import Prefetch

# Third party imports
from rest_framework.response import Response
from rest_framework import status
from sentry_sdk import capture_exception

# Module imports
from .base import BaseViewSet, BaseAPIView
from plane.api.serializers import (
    IssuePropertySerializer,
    IssuePropertyValueSerializer,
    IssuePropertyReadSerializer,
)
from plane.db.models import (
    Workspace,
    IssueProperty,
    IssuePropertyValue,
    Project,
)
from plane.api.permissions import WorkSpaceAdminPermission
from plane.bgtasks.issue_property_task import issue_property_json_task

def is_valid_uuid(uuid_string):
    try:
        uuid_obj = uuid.UUID(uuid_string)
        return str(uuid_obj) == uuid_string
    except ValueError:
        return False


class IssuePropertyViewSet(BaseViewSet):
    serializer_class = IssuePropertySerializer
    model = IssueProperty
    permission_classes = [
        WorkSpaceAdminPermission,
    ]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(workspace__slug=self.kwargs.get("slug"))
            .prefetch_related("children")
        )

    def list(self, request, slug):
        try:
            project_id = request.GET.get("project", False)
            issue_properties = self.get_queryset().filter(
                parent__isnull=True,
            )

            if project_id:
                issue_properties = issue_properties.filter(project_id=project_id)

            serializer = IssuePropertySerializer(issue_properties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            capture_exception(e)
            return Response(
                {"error": "Something went wrong please try again later"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def create(self, request, slug):
        try:
            workspace = Workspace.objects.get(slug=slug)
            serializer = IssuePropertySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(workspace_id=workspace.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Workspace.DoesNotExist:
            return Response(
                {"error": "Workspace does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            capture_exception(e)
            return Response(
                {"error": "Something went wrong please try again later"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class IssuePropertyValueViewSet(BaseViewSet):
    serializer_class = IssuePropertyValueSerializer
    model = IssuePropertyValue

    def perform_create(self, serializer):
        serializer.save(
            project_id=self.kwargs.get("project_id"),
            issue_id=self.kwargs.get("issue_id"),
            issue_property_id=self.kwargs.get("issue_property_id"),
        )

    def create(self, request, slug, project_id, issue_id):
        try:
            request_data = request.data.get("issue_properties", [])

            project = Project.objects.get(pk=project_id)
            workspace_id = project.workspace_id

            # Get all the issue_properties
            issue_properties = IssueProperty.objects.filter(
                pk__in=[prop for prop in request_data if is_valid_uuid(prop)],
                workspace__slug=slug,
            )

            bulk_issue_props = []
            for issue_property in issue_properties:
                prop_values = request_data.get(str(issue_property.id))
                if issue_property.is_multi and isinstance(prop_values, list):
                    if issue_property.type == "entity" or issue_property.type == "relation" or issue_property.type == "mselect":
                        for prop_value in prop_values:
                            bulk_issue_props.append(
                                IssuePropertyValue(
                                    values_uuid=prop_value,
                                    values=None,
                                    issue_property=issue_property,
                                    project_id=project_id,
                                    workspace_id=workspace_id,
                                    issue_id=issue_id,
                                )
                            )
                    else:
                        for prop_value in prop_values:
                            bulk_issue_props.append(
                                IssuePropertyValue(
                                    values_uuid=None,
                                    values=None,
                                    issue_property=issue_property,
                                    project_id=project_id,
                                    workspace_id=workspace_id,
                                    issue_id=issue_id,
                                )
                            )
                else:
                    if issue_property.type == "entity" or issue_property.type == "relation" or issue_property.type == "mselect":
                            bulk_issue_props.append(
                                IssuePropertyValue(
                                    values_uuid=prop_value,
                                    values=None,
                                    issue_property=issue_property,
                                    project_id=project_id,
                                    workspace_id=workspace_id,
                                    issue_id=issue_id,
                                )
                            )
                    else:
                            bulk_issue_props.append(
                                IssuePropertyValue(
                                    values_uuid=None,
                                    values=None,
                                    issue_property=issue_property,
                                    project_id=project_id,
                                    workspace_id=workspace_id,
                                    issue_id=issue_id,
                                )
                            )

            issue_property_values = IssuePropertyValue.objects.bulk_create(
                bulk_issue_props, batch_size=100, ignore_conflicts=True
            )
            # Update the JSON for the issue property
            issue_property_json_task.delay(slug=slug, project_id=project_id, issue_id=issue_id)
            serilaizer = IssuePropertyValueSerializer(issue_property_values, many=True)
            return Response(serilaizer.data, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project Does not exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong please try again later"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def list(self, request, slug, project_id, issue_id):
        try:
            issue_properties = (
                IssueProperty.objects.filter(
                    workspace__slug=slug,
                    property_values__project_id=project_id,
                )
                .prefetch_related("children")
                .prefetch_related(
                    Prefetch(
                        "property_values",
                        queryset=IssuePropertyValue.objects.filter(
                            issue_id=issue_id,
                            workspace__slug=slug,
                            project_id=project_id,
                        ),
                    )
                )
                .distinct()
            )
            serializer = IssuePropertyReadSerializer(issue_properties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            capture_exception(e)
            return Response(
                {"error": "Something went wrong please try again later"},
                status=status.HTTP_400_BAD_REQUEST,
            )
