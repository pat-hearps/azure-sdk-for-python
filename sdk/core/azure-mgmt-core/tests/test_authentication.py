#--------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#--------------------------------------------------------------------------
import base64
import itertools
import time

from azure.core.credentials import AccessToken
from azure.core.pipeline import Pipeline
from azure.mgmt.core.policies._authentication import _parse_challenges, ARMChallengeAuthenticationPolicy
from azure.core.pipeline.transport import HttpRequest

import pytest

try:
    from unittest.mock import Mock
except ImportError:
    # python < 3.3
    from mock import Mock


def test_challenge_parsing():
    challenges = (
        (  # CAE - insufficient claims
            'Bearer realm="", authorization_uri="https://login.microsoftonline.com/common/oauth2/authorize", client_id="00000003-0000-0000-c000-000000000000", error="insufficient_claims", claims="eyJhY2Nlc3NfdG9rZW4iOiB7ImZvbyI6ICJiYXIifX0="',
            {
                "authorization_uri": "https://login.microsoftonline.com/common/oauth2/authorize",
                "client_id": "00000003-0000-0000-c000-000000000000",
                "error": "insufficient_claims",
                "claims": "eyJhY2Nlc3NfdG9rZW4iOiB7ImZvbyI6ICJiYXIifX0=",
                "realm": "",
            },
        ),
        (  # CAE - sessions revoked
            'Bearer authorization_uri="https://login.windows-ppe.net/", error="invalid_token", error_description="User session has been revoked", claims="eyJhY2Nlc3NfdG9rZW4iOnsibmJmIjp7ImVzc2VudGlhbCI6dHJ1ZSwgInZhbHVlIjoiMTYwMzc0MjgwMCJ9fX0="',
            {
                "authorization_uri": "https://login.windows-ppe.net/",
                "error": "invalid_token",
                "error_description": "User session has been revoked",
                "claims": "eyJhY2Nlc3NfdG9rZW4iOnsibmJmIjp7ImVzc2VudGlhbCI6dHJ1ZSwgInZhbHVlIjoiMTYwMzc0MjgwMCJ9fX0=",
            },
        ),
        (  # CAE - IP policy
            'Bearer authorization_uri="https://login.windows.net/", error="invalid_token", error_description="Tenant IP Policy validate failed.", claims="eyJhY2Nlc3NfdG9rZW4iOnsibmJmIjp7ImVzc2VudGlhbCI6dHJ1ZSwidmFsdWUiOiIxNjEwNTYzMDA2In0sInhtc19ycF9pcGFkZHIiOnsidmFsdWUiOiIxLjIuMy40In19fQ"',
            {
                "authorization_uri": "https://login.windows.net/",
                "error": "invalid_token",
                "error_description": "Tenant IP Policy validate failed.",
                "claims": "eyJhY2Nlc3NfdG9rZW4iOnsibmJmIjp7ImVzc2VudGlhbCI6dHJ1ZSwidmFsdWUiOiIxNjEwNTYzMDA2In0sInhtc19ycF9pcGFkZHIiOnsidmFsdWUiOiIxLjIuMy40In19fQ"
            }
        ),
        (  # ARM
            'Bearer authorization_uri="https://login.windows.net/", error="invalid_token", error_description="The authentication failed because of missing \'Authorization\' header."',
            {
                "authorization_uri": "https://login.windows.net/",
                "error": "invalid_token",
                "error_description": "The authentication failed because of missing 'Authorization' header.",
            },
        ),
    )

    for challenge, expected_parameters in challenges:
        challenge = _parse_challenges(challenge)
        assert len(challenge) == 1
        assert challenge[0].scheme == "Bearer"
        assert challenge[0].parameters == expected_parameters

    for permutation in itertools.permutations(challenge for challenge, _ in challenges):
        parsed_challenges = _parse_challenges(", ".join(permutation))
        assert len(parsed_challenges) == len(challenges)
        expected_parameters = [parameters for _, parameters in challenges]
        for challenge in parsed_challenges:
            assert challenge.scheme == "Bearer"
            expected_parameters.remove(challenge.parameters)
        assert len(expected_parameters) == 0


def test_claims_challenge():
    """ARMChallengeAuthenticationPolicy should pass claims from an authentication challenge to its credential"""

    first_token = AccessToken("first", int(time.time()) + 3600)
    second_token = AccessToken("second", int(time.time()) + 3600)
    tokens = (t for t in (first_token, second_token))

    expected_claims = '{"access_token": {"essential": "true"}'
    expected_scope = "scope"

    challenge = 'Bearer authorization_uri="https://localhost", error=".", error_description=".", claims="{}"'.format(
        base64.b64encode(expected_claims.encode()).decode()
    )
    responses = (r for r in (Mock(status_code=401, headers={"WWW-Authenticate": challenge}), Mock(status_code=200)))

    def send(request):
        res = next(responses)
        if res.status_code == 401:
            expected_token = first_token.token
        else:
            expected_token = second_token.token
        assert request.headers["Authorization"] == "Bearer " + expected_token

        return res

    def get_token(*scopes, **kwargs):
        assert scopes == (expected_scope,)
        return next(tokens)

    credential = Mock(get_token=Mock(wraps=get_token))
    transport = Mock(send=Mock(wraps=send))
    policies = [ARMChallengeAuthenticationPolicy(credential, expected_scope)]
    pipeline = Pipeline(transport=transport, policies=policies)

    response = pipeline.run(HttpRequest("GET", "https://localhost"))

    assert response.http_response.status_code == 200
    assert transport.send.call_count == 2
    assert credential.get_token.call_count == 2
    credential.get_token.assert_called_with(expected_scope, claims=expected_claims)
    with pytest.raises(StopIteration):
        next(tokens)
    with pytest.raises(StopIteration):
        next(responses)