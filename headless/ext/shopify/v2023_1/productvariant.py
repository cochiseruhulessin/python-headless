# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ..resource import ShopifyResource


class ProductVariant(ShopifyResource):
    id: int
    product_id: int
    sku: str
    title: str

    class Meta:
        base_endpoint: str = '/2023-01/products/{0}/variants'
        name: str = 'variant'
        pluralname: str = 'variants'