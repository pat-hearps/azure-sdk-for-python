# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, Callable, Dict, Generic, Optional, TypeVar, Union
import warnings

from azure.core.exceptions import HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.paging import ItemPaged
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpRequest, HttpResponse
from azure.core.polling import LROPoller, NoPolling, PollingMethod
from azure.mgmt.core.exceptions import ARMErrorFormat
from azure.mgmt.core.polling.arm_polling import ARMPolling

from .. import models

T = TypeVar('T')
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

class ApplicationsOperations(object):
    """ApplicationsOperations operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~azure.mgmt.resource.managedapplications.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    def get(
        self,
        resource_group_name,  # type: str
        application_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.Application"
        """Gets the managed application.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
        :type resource_group_name: str
        :param application_name: The name of the managed application.
        :type application_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Application or the result of cls(response)
        :rtype: ~azure.mgmt.resource.managedapplications.models.Application or None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.Application"]
        error_map = kwargs.pop('error_map', {404: ResourceNotFoundError, 409: ResourceExistsError})
        api_version = "2018-06-01"

        # Construct URL
        url = self.get.metadata['url']
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
            'applicationName': self._serialize.url("application_name", application_name, 'str', max_length=64, min_length=3),
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = 'application/json'

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 404]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('Application', pipeline_response)

        if cls:
          return cls(pipeline_response, deserialized, {})

        return deserialized
    get.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Solutions/applications/{applicationName}'}

    def _delete_initial(
        self,
        resource_group_name,  # type: str
        application_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = kwargs.pop('error_map', {404: ResourceNotFoundError, 409: ResourceExistsError})
        api_version = "2018-06-01"

        # Construct URL
        url = self._delete_initial.metadata['url']
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
            'applicationName': self._serialize.url("application_name", application_name, 'str', max_length=64, min_length=3),
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]

        # Construct and send request
        request = self._client.delete(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [202, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        if cls:
          return cls(pipeline_response, None, {})

    _delete_initial.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Solutions/applications/{applicationName}'}

    def begin_delete(
        self,
        resource_group_name,  # type: str
        application_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Deletes the managed application.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
        :type resource_group_name: str
        :param application_name: The name of the managed application.
        :type application_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword polling: True for ARMPolling, False for no polling, or a
         polling object for personal polling strategy
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :return: An instance of LROPoller that returns None
        :rtype: ~azure.core.polling.LROPoller[None]

        :raises ~azure.core.exceptions.HttpResponseError:
        """
        polling = kwargs.pop('polling', True)  # type: Union[bool, PollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        raw_result = self._delete_initial(
            resource_group_name=resource_group_name,
            application_name=application_name,
            cls=lambda x,y,z: x,
            **kwargs
        )

        def get_long_running_output(pipeline_response):
            if cls:
                return cls(pipeline_response, None, {})

        lro_delay = kwargs.get(
            'polling_interval',
            self._config.polling_interval
        )
        if polling is True: polling_method = ARMPolling(lro_delay,  **kwargs)
        elif polling is False: polling_method = NoPolling()
        else: polling_method = polling
        return LROPoller(self._client, raw_result, get_long_running_output, polling_method)
    begin_delete.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Solutions/applications/{applicationName}'}

    def _create_or_update_initial(
        self,
        resource_group_name,  # type: str
        application_name,  # type: str
        parameters,  # type: "models.Application"
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.Application"
        cls = kwargs.pop('cls', None)  # type: ClsType["models.Application"]
        error_map = kwargs.pop('error_map', {404: ResourceNotFoundError, 409: ResourceExistsError})
        api_version = "2018-06-01"
        content_type = kwargs.pop("content_type", "application/json")

        # Construct URL
        url = self._create_or_update_initial.metadata['url']
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
            'applicationName': self._serialize.url("application_name", application_name, 'str', max_length=64, min_length=3),
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = 'application/json'

        # Construct and send request
        body_content_kwargs = {}  # type: Dict[str, Any]
        body_content = self._serialize.body(parameters, 'Application')
        body_content_kwargs['content'] = body_content
        request = self._client.put(url, query_parameters, header_parameters, **body_content_kwargs)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('Application', pipeline_response)

        if response.status_code == 201:
            deserialized = self._deserialize('Application', pipeline_response)

        if cls:
          return cls(pipeline_response, deserialized, {})

        return deserialized
    _create_or_update_initial.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Solutions/applications/{applicationName}'}

    def begin_create_or_update(
        self,
        resource_group_name,  # type: str
        application_name,  # type: str
        parameters,  # type: "models.Application"
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.Application"
        """Creates a new managed application.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
        :type resource_group_name: str
        :param application_name: The name of the managed application.
        :type application_name: str
        :param parameters: Parameters supplied to the create or update a managed application.
        :type parameters: ~azure.mgmt.resource.managedapplications.models.Application
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword polling: True for ARMPolling, False for no polling, or a
         polling object for personal polling strategy
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :return: An instance of LROPoller that returns Application
        :rtype: ~azure.core.polling.LROPoller[~azure.mgmt.resource.managedapplications.models.Application]

        :raises ~azure.core.exceptions.HttpResponseError:
        """
        polling = kwargs.pop('polling', True)  # type: Union[bool, PollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType["models.Application"]
        raw_result = self._create_or_update_initial(
            resource_group_name=resource_group_name,
            application_name=application_name,
            parameters=parameters,
            cls=lambda x,y,z: x,
            **kwargs
        )

        def get_long_running_output(pipeline_response):
            deserialized = self._deserialize('Application', pipeline_response)

            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized

        lro_delay = kwargs.get(
            'polling_interval',
            self._config.polling_interval
        )
        if polling is True: polling_method = ARMPolling(lro_delay,  **kwargs)
        elif polling is False: polling_method = NoPolling()
        else: polling_method = polling
        return LROPoller(self._client, raw_result, get_long_running_output, polling_method)
    begin_create_or_update.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Solutions/applications/{applicationName}'}

    def update(
        self,
        resource_group_name,  # type: str
        application_name,  # type: str
        parameters=None,  # type: Optional["models.Application"]
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.Application"
        """Updates an existing managed application. The only value that can be updated via PATCH currently is the tags.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
        :type resource_group_name: str
        :param application_name: The name of the managed application.
        :type application_name: str
        :param parameters: Parameters supplied to update an existing managed application.
        :type parameters: ~azure.mgmt.resource.managedapplications.models.Application
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Application or the result of cls(response)
        :rtype: ~azure.mgmt.resource.managedapplications.models.Application
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.Application"]
        error_map = kwargs.pop('error_map', {404: ResourceNotFoundError, 409: ResourceExistsError})
        api_version = "2018-06-01"
        content_type = kwargs.pop("content_type", "application/json")

        # Construct URL
        url = self.update.metadata['url']
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
            'applicationName': self._serialize.url("application_name", application_name, 'str', max_length=64, min_length=3),
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = 'application/json'

        # Construct and send request
        body_content_kwargs = {}  # type: Dict[str, Any]
        if parameters is not None:
            body_content = self._serialize.body(parameters, 'Application')
        else:
            body_content = None
        body_content_kwargs['content'] = body_content
        request = self._client.patch(url, query_parameters, header_parameters, **body_content_kwargs)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('Application', pipeline_response)

        if cls:
          return cls(pipeline_response, deserialized, {})

        return deserialized
    update.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Solutions/applications/{applicationName}'}

    def list_by_resource_group(
        self,
        resource_group_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.ApplicationListResult"
        """Gets all the applications within a resource group.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
        :type resource_group_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ApplicationListResult or the result of cls(response)
        :rtype: ~azure.mgmt.resource.managedapplications.models.ApplicationListResult
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.ApplicationListResult"]
        error_map = kwargs.pop('error_map', {404: ResourceNotFoundError, 409: ResourceExistsError})
        api_version = "2018-06-01"

        def prepare_request(next_link=None):
            if not next_link:
                # Construct URL
                url = self.list_by_resource_group.metadata['url']
                path_format_arguments = {
                    'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
                    'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
                }
                url = self._client.format_url(url, **path_format_arguments)
            else:
                url = next_link

            # Construct parameters
            query_parameters = {}  # type: Dict[str, Any]
            query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

            # Construct headers
            header_parameters = {}  # type: Dict[str, Any]
            header_parameters['Accept'] = 'application/json'

            # Construct and send request
            request = self._client.get(url, query_parameters, header_parameters)
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize('ApplicationListResult', pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                error = self._deserialize(models.ErrorResponse, response)
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response

        return ItemPaged(
            get_next, extract_data
        )
    list_by_resource_group.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Solutions/applications'}

    def list_by_subscription(
        self,
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.ApplicationListResult"
        """Gets all the applications within a subscription.

        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: ApplicationListResult or the result of cls(response)
        :rtype: ~azure.mgmt.resource.managedapplications.models.ApplicationListResult
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.ApplicationListResult"]
        error_map = kwargs.pop('error_map', {404: ResourceNotFoundError, 409: ResourceExistsError})
        api_version = "2018-06-01"

        def prepare_request(next_link=None):
            if not next_link:
                # Construct URL
                url = self.list_by_subscription.metadata['url']
                path_format_arguments = {
                    'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
                }
                url = self._client.format_url(url, **path_format_arguments)
            else:
                url = next_link

            # Construct parameters
            query_parameters = {}  # type: Dict[str, Any]
            query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

            # Construct headers
            header_parameters = {}  # type: Dict[str, Any]
            header_parameters['Accept'] = 'application/json'

            # Construct and send request
            request = self._client.get(url, query_parameters, header_parameters)
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize('ApplicationListResult', pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                error = self._deserialize(models.ErrorResponse, response)
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response

        return ItemPaged(
            get_next, extract_data
        )
    list_by_subscription.metadata = {'url': '/subscriptions/{subscriptionId}/providers/Microsoft.Solutions/applications'}

    def get_by_id(
        self,
        application_id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.Application"
        """Gets the managed application.

        :param application_id: The fully qualified ID of the managed application, including the managed
         application name and the managed application resource type. Use the format,
         /subscriptions/{guid}/resourceGroups/{resource-group-
         name}/Microsoft.Solutions/applications/{application-name}.
        :type application_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Application or the result of cls(response)
        :rtype: ~azure.mgmt.resource.managedapplications.models.Application or None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.Application"]
        error_map = kwargs.pop('error_map', {404: ResourceNotFoundError, 409: ResourceExistsError})
        api_version = "2018-06-01"

        # Construct URL
        url = self.get_by_id.metadata['url']
        path_format_arguments = {
            'applicationId': self._serialize.url("application_id", application_id, 'str', skip_quote=True),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = 'application/json'

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 404]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('Application', pipeline_response)

        if cls:
          return cls(pipeline_response, deserialized, {})

        return deserialized
    get_by_id.metadata = {'url': '/{applicationId}'}

    def _delete_by_id_initial(
        self,
        application_id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = kwargs.pop('error_map', {404: ResourceNotFoundError, 409: ResourceExistsError})
        api_version = "2018-06-01"

        # Construct URL
        url = self._delete_by_id_initial.metadata['url']
        path_format_arguments = {
            'applicationId': self._serialize.url("application_id", application_id, 'str', skip_quote=True),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]

        # Construct and send request
        request = self._client.delete(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [202, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        if cls:
          return cls(pipeline_response, None, {})

    _delete_by_id_initial.metadata = {'url': '/{applicationId}'}

    def begin_delete_by_id(
        self,
        application_id,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Deletes the managed application.

        :param application_id: The fully qualified ID of the managed application, including the managed
     application name and the managed application resource type. Use the format,
     /subscriptions/{guid}/resourceGroups/{resource-group-
     name}/Microsoft.Solutions/applications/{application-name}.
        :type application_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword polling: True for ARMPolling, False for no polling, or a
         polling object for personal polling strategy
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :return: An instance of LROPoller that returns None
        :rtype: ~azure.core.polling.LROPoller[None]

        :raises ~azure.core.exceptions.HttpResponseError:
        """
        polling = kwargs.pop('polling', True)  # type: Union[bool, PollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        raw_result = self._delete_by_id_initial(
            application_id=application_id,
            cls=lambda x,y,z: x,
            **kwargs
        )

        def get_long_running_output(pipeline_response):
            if cls:
                return cls(pipeline_response, None, {})

        lro_delay = kwargs.get(
            'polling_interval',
            self._config.polling_interval
        )
        if polling is True: polling_method = ARMPolling(lro_delay,  **kwargs)
        elif polling is False: polling_method = NoPolling()
        else: polling_method = polling
        return LROPoller(self._client, raw_result, get_long_running_output, polling_method)
    begin_delete_by_id.metadata = {'url': '/{applicationId}'}

    def _create_or_update_by_id_initial(
        self,
        application_id,  # type: str
        parameters,  # type: "models.Application"
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.Application"
        cls = kwargs.pop('cls', None)  # type: ClsType["models.Application"]
        error_map = kwargs.pop('error_map', {404: ResourceNotFoundError, 409: ResourceExistsError})
        api_version = "2018-06-01"
        content_type = kwargs.pop("content_type", "application/json")

        # Construct URL
        url = self._create_or_update_by_id_initial.metadata['url']
        path_format_arguments = {
            'applicationId': self._serialize.url("application_id", application_id, 'str', skip_quote=True),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = 'application/json'

        # Construct and send request
        body_content_kwargs = {}  # type: Dict[str, Any]
        body_content = self._serialize.body(parameters, 'Application')
        body_content_kwargs['content'] = body_content
        request = self._client.put(url, query_parameters, header_parameters, **body_content_kwargs)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('Application', pipeline_response)

        if response.status_code == 201:
            deserialized = self._deserialize('Application', pipeline_response)

        if cls:
          return cls(pipeline_response, deserialized, {})

        return deserialized
    _create_or_update_by_id_initial.metadata = {'url': '/{applicationId}'}

    def begin_create_or_update_by_id(
        self,
        application_id,  # type: str
        parameters,  # type: "models.Application"
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.Application"
        """Creates a new managed application.

        :param application_id: The fully qualified ID of the managed application, including the managed
     application name and the managed application resource type. Use the format,
     /subscriptions/{guid}/resourceGroups/{resource-group-
     name}/Microsoft.Solutions/applications/{application-name}.
        :type application_id: str
        :param parameters: Parameters supplied to the create or update a managed application.
        :type parameters: ~azure.mgmt.resource.managedapplications.models.Application
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword polling: True for ARMPolling, False for no polling, or a
         polling object for personal polling strategy
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :return: An instance of LROPoller that returns Application
        :rtype: ~azure.core.polling.LROPoller[~azure.mgmt.resource.managedapplications.models.Application]

        :raises ~azure.core.exceptions.HttpResponseError:
        """
        polling = kwargs.pop('polling', True)  # type: Union[bool, PollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType["models.Application"]
        raw_result = self._create_or_update_by_id_initial(
            application_id=application_id,
            parameters=parameters,
            cls=lambda x,y,z: x,
            **kwargs
        )

        def get_long_running_output(pipeline_response):
            deserialized = self._deserialize('Application', pipeline_response)

            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized

        lro_delay = kwargs.get(
            'polling_interval',
            self._config.polling_interval
        )
        if polling is True: polling_method = ARMPolling(lro_delay,  **kwargs)
        elif polling is False: polling_method = NoPolling()
        else: polling_method = polling
        return LROPoller(self._client, raw_result, get_long_running_output, polling_method)
    begin_create_or_update_by_id.metadata = {'url': '/{applicationId}'}

    def update_by_id(
        self,
        application_id,  # type: str
        parameters=None,  # type: Optional["models.Application"]
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.Application"
        """Updates an existing managed application. The only value that can be updated via PATCH currently is the tags.

        :param application_id: The fully qualified ID of the managed application, including the managed
         application name and the managed application resource type. Use the format,
         /subscriptions/{guid}/resourceGroups/{resource-group-
         name}/Microsoft.Solutions/applications/{application-name}.
        :type application_id: str
        :param parameters: Parameters supplied to update an existing managed application.
        :type parameters: ~azure.mgmt.resource.managedapplications.models.Application
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Application or the result of cls(response)
        :rtype: ~azure.mgmt.resource.managedapplications.models.Application
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.Application"]
        error_map = kwargs.pop('error_map', {404: ResourceNotFoundError, 409: ResourceExistsError})
        api_version = "2018-06-01"
        content_type = kwargs.pop("content_type", "application/json")

        # Construct URL
        url = self.update_by_id.metadata['url']
        path_format_arguments = {
            'applicationId': self._serialize.url("application_id", application_id, 'str', skip_quote=True),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = 'application/json'

        # Construct and send request
        body_content_kwargs = {}  # type: Dict[str, Any]
        if parameters is not None:
            body_content = self._serialize.body(parameters, 'Application')
        else:
            body_content = None
        body_content_kwargs['content'] = body_content
        request = self._client.patch(url, query_parameters, header_parameters, **body_content_kwargs)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('Application', pipeline_response)

        if cls:
          return cls(pipeline_response, deserialized, {})

        return deserialized
    update_by_id.metadata = {'url': '/{applicationId}'}
