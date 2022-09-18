from unittest import TestCase
from fastapi.testclient import TestClient
from main import app as web_app


class ApiTestCase(TestCase):

    def setUp(self):
        self.client = TestClient(web_app)

    def test_main_url(self):
        response = self.client.get('/')
        check_resp = {"message":"Deliveries server"}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), check_resp)

    def test_workflow(self):
        # test create delivery
        payload_delivery = {"type":"CREATE_DELIVERY","data":{"budget":"50","notes":"Pick 3 ice creams"}}
        response = self.client.post('/deliveries', json=payload_delivery)
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertEqual(list(json_resp.keys()), ['id', 'budget', 'notes', 'status'])
        self.assertEqual(json_resp['status'], 'ready')
        self.assertEqual(str(json_resp['budget']), payload_delivery['data']['budget'])
        self.assertEqual(json_resp['notes'], payload_delivery['data']['notes'])

        delivery_id = json_resp['id']

        # test start delivery
        payload_event = {"delivery_id": delivery_id,"type":"START_DELIVERY","data":{}}
        response = self.client.post('/event', json=payload_event)
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertEqual(list(json_resp.keys()), ['id', 'budget', 'notes', 'status'])
        self.assertEqual(json_resp['status'], 'active')
        self.assertEqual(str(json_resp['budget']), str(payload_delivery['data']['budget']))
        self.assertEqual(json_resp['notes'], payload_delivery['data']['notes'])

        # start delivery again
        response = self.client.post('/event', json=payload_event)
        self.assertEqual(response.status_code, 400)
        json_resp = response.json()
        self.assertEqual(json_resp['detail'], 'Delivery already started')

        # pickup product with not enough budget
        payload_event = {"delivery_id":delivery_id,"type":"PICKUP_PRODUCTS","data":{"quantity":"3","purchase_price":"20"}}
        response = self.client.post('/event', json=payload_event)
        self.assertEqual(response.status_code, 400)
        json_resp = response.json()
        self.assertEqual(json_resp['detail'], 'Not enough budget')

        # increase budget on 20
        add_budget = 20
        payload_event = {"delivery_id":delivery_id,"type":"INCREASE_BUDGET","data":{"budget":str(add_budget)}}
        response = self.client.post('/event', json=payload_event)
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertEqual(list(json_resp.keys()), ['id', 'budget', 'notes', 'status'])
        self.assertEqual(json_resp['status'], 'active')
        updated_budget = int(payload_event['data']['budget']) + int(payload_delivery['data']['budget'])
        self.assertEqual(str(json_resp['budget']), str(updated_budget), 'Check budget')
        self.assertEqual(json_resp['notes'], payload_delivery['data']['notes'])

        # repeat pickup product with enough budget
        last_quantity = 3
        payload_event = {"delivery_id":delivery_id,"type":"PICKUP_PRODUCTS","data":{"quantity":str(last_quantity),"purchase_price":"20"}}
        response = self.client.post('/event', json=payload_event)
        json_resp = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(json_resp.keys()), ['id', 'budget', 'notes', 'status', 'purchase_price', 'quantity'])
        self.assertEqual(json_resp['status'], 'collected')
        after_pick_budget = updated_budget - int(payload_event['data']['quantity'])*int(payload_event['data']['purchase_price'])
        self.assertEqual(str(json_resp['budget']), str(after_pick_budget))
        self.assertEqual(json_resp['notes'], payload_delivery['data']['notes'])
        self.assertEqual(str(json_resp['quantity']), payload_event['data']['quantity'])

        # wrong deliver products
        payload_event = {"delivery_id":delivery_id,"type":"DELIVER_PRODUCTS","data":{"quantity":"4","sell_price":"25"}}
        response = self.client.post('/event', json=payload_event)
        json_resp = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_resp['detail'], 'Not enough quantity')

        # ok deliver products
        payload_event = {"delivery_id":delivery_id,"type":"DELIVER_PRODUCTS","data":{"quantity":"3","sell_price":"25"}}
        response = self.client.post('/event', json=payload_event)
        json_resp = response.json()
        self.assertEqual(list(json_resp.keys()), ['id', 'budget', 'notes', 'status', 'purchase_price', 'quantity', 'sell_price'])
        self.assertEqual(json_resp['status'], 'completed')
        final_budget = after_pick_budget + int(payload_event['data']['quantity'])*int(payload_event['data']['sell_price'])
        self.assertEqual(str(json_resp['budget']), str(final_budget))
        self.assertEqual(json_resp['notes'], payload_delivery['data']['notes'])
        self.assertEqual(str(json_resp['quantity']), str(int(last_quantity) - int(payload_event['data']['quantity'])))
