# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

from headless.core import Resource


class User(Resource):
    iduser: int
    username: str
    firstname: str
    lastname: str
    emailaddress: str

    # Mismatch with docs: language can be null
    language: str | None
    admin: bool
    active: bool
    last_login_at: datetime.datetime | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None = None

    class Meta:
        base_endpoint: str = '/v1/users'