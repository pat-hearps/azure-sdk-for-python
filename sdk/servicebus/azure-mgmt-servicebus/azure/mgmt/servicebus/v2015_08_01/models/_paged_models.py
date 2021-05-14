# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.paging import Paged


class OperationPaged(Paged):
    """
    A paging container for iterating over a list of :class:`Operation <azure.mgmt.servicebus.v2015_08_01.models.Operation>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[Operation]'}
    }

    def __init__(self, *args, **kwargs):

        super(OperationPaged, self).__init__(*args, **kwargs)
class NamespaceResourcePaged(Paged):
    """
    A paging container for iterating over a list of :class:`NamespaceResource <azure.mgmt.servicebus.v2015_08_01.models.NamespaceResource>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[NamespaceResource]'}
    }

    def __init__(self, *args, **kwargs):

        super(NamespaceResourcePaged, self).__init__(*args, **kwargs)
class SharedAccessAuthorizationRuleResourcePaged(Paged):
    """
    A paging container for iterating over a list of :class:`SharedAccessAuthorizationRuleResource <azure.mgmt.servicebus.v2015_08_01.models.SharedAccessAuthorizationRuleResource>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[SharedAccessAuthorizationRuleResource]'}
    }

    def __init__(self, *args, **kwargs):

        super(SharedAccessAuthorizationRuleResourcePaged, self).__init__(*args, **kwargs)
class QueueResourcePaged(Paged):
    """
    A paging container for iterating over a list of :class:`QueueResource <azure.mgmt.servicebus.v2015_08_01.models.QueueResource>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[QueueResource]'}
    }

    def __init__(self, *args, **kwargs):

        super(QueueResourcePaged, self).__init__(*args, **kwargs)
class TopicResourcePaged(Paged):
    """
    A paging container for iterating over a list of :class:`TopicResource <azure.mgmt.servicebus.v2015_08_01.models.TopicResource>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[TopicResource]'}
    }

    def __init__(self, *args, **kwargs):

        super(TopicResourcePaged, self).__init__(*args, **kwargs)
class SubscriptionResourcePaged(Paged):
    """
    A paging container for iterating over a list of :class:`SubscriptionResource <azure.mgmt.servicebus.v2015_08_01.models.SubscriptionResource>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[SubscriptionResource]'}
    }

    def __init__(self, *args, **kwargs):

        super(SubscriptionResourcePaged, self).__init__(*args, **kwargs)