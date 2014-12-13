from django.test import TestCase
from oscar.core.loading import get_model
import json
from common.factories import create_order
from user.models import TinvilleUser
from designer_shop.models import Shop


ShippingEvent = get_model('order', 'ShippingEvent')
ShippingEventType = get_model('order', 'ShippingEventType')

class PackageStatusTest(TestCase):
    fixtures = ['all.json']

    def setUp(self):
        self.user = TinvilleUser.objects.create(email="tony.stark@StarkIndustries.com")
        self.shop = Shop.objects.create(name='StarkIndustries', user=self.user)
        self.order = create_order(number="2-10001", user=self.user, shop=self.shop)

        self.shipped_event = self.order.shipping_events.create(
            event_type=ShippingEventType.objects.get(code="shipped"), group=0, tracking_code='EZ4000000004', reference='foo')
        validEasyPostRequest = {
            "id": "evt_qatAiJDM",
            "object": "Event",
            "created_at": "2014-11-19T10:51:54Z",
            "updated_at": "2014-11-19T10:51:54Z",
            "description": "tracker.updated",
            "mode": "test",
            "previous_attributes": {
                "status": "unknown"
            },
            "pending_urls": [],
            "completed_urls": [],
            "result": {
                "id": "trk_Txyy1vaM",
                "object": "Tracker",
                "mode": "test",
                "tracking_code": "EZ4000000004",
                "status": "in_transit",
                "created_at": "2014-11-18T10:51:54Z",
                "updated_at": "2014-11-19T10:51:54Z",
                "signed_by": "John Tester",
                "weight": 17.6,
                "est_delivery_date": "2014-08-27T00:00:00Z",
                "shipment_id": "",
                "carrier": "UPS",
                "tracking_details": [
                    {
                        "object": "TrackingDetail",
                        "message": "BILLING INFORMATION RECEIVED",
                        "status": "pre_transit",
                        "datetime": "2014-11-21T14:24:00Z",
                        "tracking_location": {
                            "object": "TrackingLocation",
                            "city": None,
                            "state": None,
                            "country": None,
                            "zip": None
                        }
                    }
                ]
            }
        }

        self.validEasyPostRequest = json.dumps(validEasyPostRequest)
        self.requestUrl = '/packageStatus'


    def tearDown(self):
        pass

    def test_package_status(self):
        result = self.client.post(self.requestUrl, self.validEasyPostRequest, content_type="application/json")
        self.assertEqual(result.status_code, 200, "Because the service should return a 200")
        self.assertEqual(result.reason_phrase, 'OK', "Because the service should return OK")

        in_transit_event = ShippingEvent.objects.get(event_type=ShippingEventType.objects.get(code="in_transit"), tracking_code='EZ4000000004')
        self.assertEqual(self.shipped_event.group, in_transit_event.group)
        self.assertEqual(self.shipped_event.tracking_code, in_transit_event.tracking_code)
        self.assertEqual(ShippingEventType.objects.get(code="in_transit"), in_transit_event.event_type)

    def test_duplicate_package_status(self):
         result = self.client.post(self.requestUrl, self.validEasyPostRequest, content_type="application/json")
         self.assertEqual(result.status_code, 200, "Because the service should return a 200")
         self.assertEqual(result.reason_phrase, 'OK', "Because the service should return OK")

         result2 = self.client.post(self.requestUrl, self.validEasyPostRequest, content_type="application/json")
         in_transit_event = ShippingEvent.objects.get(event_type=ShippingEventType.objects.get(code="in_transit"), tracking_code='EZ4000000004')
         self.assertEqual(self.shipped_event.group, in_transit_event.group)
         self.assertEqual(self.shipped_event.tracking_code, in_transit_event.tracking_code)
         self.assertEqual(ShippingEventType.objects.get(code="in_transit"), in_transit_event.event_type)


    def test_StringEmpty_package(self):
        result = self.client.post(self.requestUrl, "", content_type="application/json")
        self.assertEqual(result.status_code, 400, "Because the service should return a 400")
        self.assertEqual(result.reason_phrase, 'BadRequest', "Because the service should return BadRequest")

    def test_StringWhitespace_package(self):
        result = self.client.post(self.requestUrl, " ", content_type="application/json")
        self.assertEqual(result.status_code, 400, "Because the service should return a 400")
        self.assertEqual(result.reason_phrase, 'BadRequest', "Because the service should return BadRequest")

    def test_emptyJson_package(self):
        result = self.client.post(self.requestUrl, json.dumps({}), content_type="application/json")
        self.assertEqual(result.status_code, 400, "Because the service should return a 400")
        self.assertEqual(result.reason_phrase, 'BadRequest', "Because the service should return BadRequest")

    def test_empty_result_package(self):
        result = self.client.post(self.requestUrl, json.dumps({"result": {}}), content_type="application/json")
        self.assertEqual(result.status_code, 400, "Because the service should return a 400")
        self.assertEqual(result.reason_phrase, 'BadRequest', "Because the service should return BadRequest")

    def test_none_result_package(self):
        result = self.client.post(self.requestUrl, json.dumps({"result": None}), content_type="application/json")
        self.assertEqual(result.status_code, 400, "Because the service should return a 400")
        self.assertEqual(result.reason_phrase, 'BadRequest', "Because the service should return BadRequest")

    def test_none_tracking_code_package(self):
        result = self.client.post(self.requestUrl, json.dumps({"result": { "tracking_code": None, "status": "in_transit"}}), content_type="application/json")
        self.assertEqual(result.status_code, 400, "Because the service should return a 400")
        self.assertEqual(result.reason_phrase, 'BadRequest', "Because the service should return BadRequest")
