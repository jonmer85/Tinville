from django.test import TestCase
from oscar.core.loading import get_model
import json
from common.factories import create_order
from user.models import TinvilleUser
from designer_shop.models import Shop
from oscar.apps.address.abstract_models import AbstractAddress
from custom_oscar.apps.dashboard.orders.views import EasyPostAddressFormatter


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
        for line in self.order.lines.all():
                self.shipped_event.line_quantities.create(line=line, quantity=line.quantity)
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
        self.assertEqual(len(in_transit_event.lines.all()), len(self.shipped_event.lines.all()), "Because in transit event should have the same lines as shipped event")
        self.assertGreater(len(in_transit_event.lines.all()), 0, "Because in transit event should have at least 1 line")
        self.assertEqual(self.shipped_event.group, in_transit_event.group, "Because the groups should be the same")
        self.assertEqual(self.shipped_event.tracking_code, in_transit_event.tracking_code, "Because the tracking code should be equal")
        self.assertEqual(ShippingEventType.objects.get(code="in_transit"), in_transit_event.event_type, "Because the Event Type should be in transit")

    def test_duplicate_package_status(self):
         result = self.client.post(self.requestUrl, self.validEasyPostRequest, content_type="application/json")
         self.assertEqual(result.status_code, 200, "Because the service should return a 200")
         self.assertEqual(result.reason_phrase, 'OK', "Because the service should return OK")

         result2 = self.client.post(self.requestUrl, self.validEasyPostRequest, content_type="application/json")
         in_transit_event = ShippingEvent.objects.get(event_type=ShippingEventType.objects.get(code="in_transit"), tracking_code='EZ4000000004')

         self.assertEqual(self.shipped_event.group, in_transit_event.group, "Because the groups should be the same")
         self.assertEqual(self.shipped_event.tracking_code, in_transit_event.tracking_code, "Because the tracking code should be equal")
         self.assertEqual(ShippingEventType.objects.get(code="in_transit"), in_transit_event.event_type, "Because the Event Type should be in transit")


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
        result = self.client.post(self.requestUrl, json.dumps({"result": { "tracking_code": None, "carrier": "USPS", "status": "in_transit"}}), content_type="application/json")
        self.assertEqual(result.status_code, 400, "Because the service should return a 400")
        self.assertEqual(result.reason_phrase, 'BadRequest', "Because the service should return BadRequest")

class EasyPostAddressTest(TestCase):

    def Valid_Address(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel', line1='800 Federal St', line2='', line4='Andover', state='MA', postcode='01810')

        easyPostAdddress = EasyPostAddressFormatter(address)
        self.assertIn('name', easyPostAdddress)
        self.assertEqual(easyPostAdddress['name'], address.name)
        self.assertIn('street1', easyPostAdddress)
        self.assertEqual(easyPostAdddress['street1'], address.line1)
        self.assertIn('street2', easyPostAdddress)
        self.assertEqual(easyPostAdddress['street2'], address.line2)
        self.assertIn('city', easyPostAdddress)
        self.assertEqual(easyPostAdddress['city'], address.city)
        self.assertIn('state', easyPostAdddress)
        self.assertEqual(easyPostAdddress['state'], address.state)
        self.assertIn('zip', easyPostAdddress)
        self.assertEqual(easyPostAdddress['zip'], address.postcode)

    def None_Name_Property(self):
        address = AbstractAddress(line1='800 Federal St', line2='', line4='Andover', state='MA', postcode='01810')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def Empty_Name_Property(self):
        address = AbstractAddress(first_name='', last_name='',line1='800 Federal St', line2='', line4='Andover', state='MA', postcode='01810')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def Whitespace_Name_Property(self):
        address = AbstractAddress(first_name=' ', last_name=' ',line1='800 Federal St', line2='', line4='Andover', state='MA', postcode='01810')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def None_Line1_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel', line2='', line4='Andover', state='MA', postcode='01810')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def Empty_Line1_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel', line1='', line2='', line4='Andover', state='MA', postcode='01810')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def Whitespace_Line1_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel', line1=' ', line2='', line4='Andover', state='MA', postcode='01810')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def None_Line2_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel', line1='123 elm', line4='Andover', state='MA', postcode='01810')
        easyPostAdddress = EasyPostAddressFormatter(address)
        self.assertIn('street2', easyPostAdddress)
        self.assertEqual(easyPostAdddress['street2'], address.line2)

    def Empty_Line2_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel', line1='123 elm', line2='', line4='Andover', state='MA', postcode='01810')
        easyPostAdddress = EasyPostAddressFormatter(address)
        self.assertIn('street2', easyPostAdddress)
        self.assertEqual(easyPostAdddress['street2'], address.line2)

    def Whitespace_Line2_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel', line1='123 elm', line2=' ', line4='Andover', state='MA', postcode='01810')
        easyPostAdddress = EasyPostAddressFormatter(address)
        self.assertIn('street2', easyPostAdddress)
        self.assertEqual(easyPostAdddress['street2'], address.line2)

    def None_City_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel',line1='800 Federal St', line2='', state='MA', postcode='01810')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def Empty_City_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel',line1='800 Federal St', line2='', line4='', state='MA', postcode='01810')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def Whitespace_City_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel',line1='800 Federal St', line2='', line4=' ', state='MA', postcode='01810')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def None_State_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel',line1='800 Federal St', line2='', line4='Andover', postcode='01810')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def Empty_State_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel',line1='800 Federal St', line2='', line4='Andover', state='', postcode='01810')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def Whitespace_State_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel',line1='800 Federal St', line2='', line4='Andover', state=' ', postcode='01810')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def None_PostCode_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel',line1='800 Federal St', line2='', line4='Andover', state='MA')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def Empty_PostCode_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel',line1='800 Federal St', line2='', line4='Andover', state='MA', postcode='')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)

    def Whitespace_PostCode_Property(self):
        address = AbstractAddress(first_name='Bob', last_name='Doel',line1='800 Federal St', line2='', line4='Andover', state='MA', postcode=' ')
        self.assertRaises(ValueError, EasyPostAddressFormatter, address=address)