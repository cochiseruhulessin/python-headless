# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

from .picqerresource import PicqerResource
from .receiptproduct import ReceiptProduct
from .receiptpurchaseorder import ReceiptPurchaseOrder
from .receiptsupplier import ReceiptSupplier
from .userreference import UserReference


class Receipt(PicqerResource):
    idreceipt: int
    idwarehouse: int | None = None
    supplier: ReceiptSupplier | None = None
    purchaseorder: ReceiptPurchaseOrder | None = None
    receiptid: str
    status: str
    remarks: str | None = None
    completed_by: UserReference | None = None
    amount_received: int = 0
    amount_received_excessive: int = 0
    completed_at: datetime.datetime | None = None
    created: datetime.datetime
    products: list[ReceiptProduct] = []

    async def receive(self, product_id: int, amount: int = 1) -> None:
        for product in self.products:
            if product.idproduct != product_id:
                continue
            response = await self._client.put(
                url=f'{self.get_persist_url()}/products/{product.idreceipt_product}',
                json={'delta': amount}
            )
            response.raise_for_status()
            break
        else:
            response = await self._client.post(
                url=f'{self.get_persist_url()}/products',
                json={'idproduct': product_id, 'force': True}
            )
            response.raise_for_status()

    async def complete(self) -> None:
        response = await self._client.put(
            url=self.get_persist_url(),
            json={"status": "completed"}
        )
        response.raise_for_status()

    async def mark_all_received(self) -> None:
        response = await self._client.post(
            url=f'{self.get_persist_url()}/mark-all-received'
        )
        response.raise_for_status()

    def get_persist_url(self) -> str:
        return self.get_retrieve_url(self.idreceipt)

    class Meta:
        base_endpoint: str = '/v1/receipts'