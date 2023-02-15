# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from headless.core import Resource


class ShopifyResource(Resource):
    __abstract__: bool = True

    @classmethod
    def process_response(
        cls,
        action: str,
        data: dict[str, Any]
    ) -> dict[str, Any]:
        if action in {'list'}:
            k = cls._meta.pluralname
        elif action in {'retrieve'}:
            k = cls._meta.name
        return data[str.lower(k)]