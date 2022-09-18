import json
from redis_connect import Delivery, Event, redis
from starlette.requests import Request
import consumers
import uvicorn
from init import app


def store_delivery(pk, delivery):
  redis.set(f'delivery:{pk}', json.dumps(delivery))

def get_delivery(pk):
  return json.loads(str(redis.get(f'delivery:{pk}')))

def build_state(pk: str):
  pks = Event.all_pks()
  all_events = [Event.get(pk) for pk in pks]
  events = [ev for ev in all_events if ev.delivery_id == pk]
  state = {}
  for event in events:
    state = consumers.CONSUMERS[event.type](state, event)
  return state

@app.get('/')
async def root():
  return {'message': 'Deliveries server'}

@app.get('/deliveries/{pk}')
async def get_state(pk: str):
  state = get_delivery(pk)
  if state is None:
    return build_state(pk)
  return state


@app.post('/deliveries')
async def create(request: Request):
  body = await request.json()
  delivery = Delivery(budget=body['data']['budget'], notes=body['data']['notes']).save()
  event = Event(delivery_id=delivery.pk, type=body['type'], data=json.dumps(body['data'])).save()
  state = consumers.CONSUMERS[event.type]({}, event)
  store_delivery(delivery.pk, state)
  return state


@app.post('/event')
async def dispatch(request: Request):
  body = await request.json()
  delivery_id = body['delivery_id']
  event = Event(delivery_id=delivery_id, type=body['type'], data=json.dumps(body['data'])).save()
  state = await get_state(delivery_id)
  new_state = consumers.CONSUMERS[body['type']](state, event)
  store_delivery(delivery_id, new_state)
  return new_state


if __name__ == "__main__":
      uvicorn.run(app)
