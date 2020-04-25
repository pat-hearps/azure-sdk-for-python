# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from typing import Any, Optional

from azure.mgmt.core import ARMPipelineClient
from msrest import Deserializer, Serializer

from ._configuration import PolicyClientConfiguration
from .operations import PolicyAssignmentsOperations
from .operations import PolicyDefinitionsOperations
from .operations import PolicySetDefinitionsOperations
from . import models


class PolicyClient(object):
    """To manage and control access to your resources, you can define customized policies and assign them at a scope.

    :ivar policy_assignments: PolicyAssignmentsOperations operations
    :vartype policy_assignments: azure.mgmt.resource.policy.v2019_01_01.operations.PolicyAssignmentsOperations
    :ivar policy_definitions: PolicyDefinitionsOperations operations
    :vartype policy_definitions: azure.mgmt.resource.policy.v2019_01_01.operations.PolicyDefinitionsOperations
    :ivar policy_set_definitions: PolicySetDefinitionsOperations operations
    :vartype policy_set_definitions: azure.mgmt.resource.policy.v2019_01_01.operations.PolicySetDefinitionsOperations
    :param credential: Credential needed for the client to connect to Azure.
    :type credential: azure.core.credentials.TokenCredential
    :param subscription_id: The ID of the target subscription.
    :type subscription_id: str
    :param str base_url: Service URL
    """

    def __init__(
        self,
        credential,  # type: "TokenCredential"
        subscription_id,  # type: str
        base_url=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        if not base_url:
            base_url = 'https://management.azure.com'
        self._config = PolicyClientConfiguration(credential, subscription_id, **kwargs)
        self._client = ARMPipelineClient(base_url=base_url, config=self._config, **kwargs)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.policy_assignments = PolicyAssignmentsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.policy_definitions = PolicyDefinitionsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.policy_set_definitions = PolicySetDefinitionsOperations(
            self._client, self._config, self._serialize, self._deserialize)

    def close(self):
        # type: () -> None
        self._client.close()

    def __enter__(self):
        # type: () -> PolicyClient
        self._client.__enter__()
        return self

    def __exit__(self, *exc_details):
        # type: (Any) -> None
        self._client.__exit__(*exc_details)
