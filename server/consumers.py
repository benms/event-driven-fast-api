from fastapi import HTTPException
import json
from redis_om import HashModel


def create_delivery(state: dict, event: HashModel):
  data = json.loads(event.data)
  return {
    'id': event.delivery_id,
    'budget': int(data['budget']),
    'notes': data['notes'],
    'status': 'ready',
  }

def start_delivery(state: dict, event: HashModel):
  if state['status'] != 'ready':
    raise HTTPException(status_code=400, detail='Delivery already started')

  return {
    **state,
    "status": "active"
  }

def pickup_products(state: dict, event: HashModel):
  data = json.loads(event.data)
  new_budget = state['budget'] - int(data['purchase_price']) * int(data['quantity'])
  if new_budget < 0:
    raise HTTPException(status_code=400, detail='Not enough budget')

  return {
    **state,
    "budget": new_budget,
    "purchase_price": int(data['purchase_price']),
    "quantity": int(data['quantity']),
    "status": 'collected',
  }

def deliver_products(state: dict, event: HashModel):
  data = json.loads(event.data)
  new_budget = state['budget'] + int(data['sell_price']) * int(data['quantity'])
  new_quantity = state['quantity'] - int(data['quantity'])
  if new_quantity < 0:
    raise HTTPException(status_code=400, detail='Not enough quantity')

  return {
    **state,
    "budget": new_budget,
    "sell_price": int(data['sell_price']),
    "quantity": new_quantity,
    "status": 'completed',
  }

def increase_budget(state: dict, event):
  data = json.loads(event.data)
  state['budget'] += int(data['budget'])
  return state


CREATE_DELIVERY = 'CREATE_DELIVERY'
START_DELIVERY = 'START_DELIVERY'
PICKUP_PRODUCTS = 'PICKUP_PRODUCTS'
DELIVER_PRODUCTS = 'DELIVER_PRODUCTS'
INCREASE_BUDGET = 'INCREASE_BUDGET'

CONSUMERS = {
  CREATE_DELIVERY: create_delivery,
  START_DELIVERY: start_delivery,
  PICKUP_PRODUCTS: pickup_products,
  DELIVER_PRODUCTS: deliver_products,
  INCREASE_BUDGET: increase_budget,
}
