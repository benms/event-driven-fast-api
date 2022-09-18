import React, { useEffect, useState } from "react";

export const CREATE_DELIVERY = 'CREATE_DELIVERY';
const START_DELIVERY = 'START_DELIVERY';
const PICKUP_PRODUCTS = 'PICKUP_PRODUCTS';
const DELIVER_PRODUCTS = 'DELIVER_PRODUCTS';
const INCREASE_BUDGET = 'INCREASE_BUDGET';

export default function Delivery(props) {
  const [state, setState] = useState({});
  const [refresh, setRefresh] = useState(false);

  useEffect(() => {
    (async () => {
      const resp = await fetch(`http://localhost:8000/deliveries/${props.id}`,{
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await resp.json();
      setState(data);
    })();
  }, [refresh]);

  const submit = async (type, e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    const data = Object.fromEntries(form.entries());
    const resp = await fetch('http://localhost:8000/event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        delivery_id: state.id,
        type,
        data,
      })
    });

    if (!resp.ok) {
      const { detail } = await resp.json();
      alert(detail);
      return;
    }

    setRefresh((s) => !s);
  };


  return <div className="row w-100">
    <div className="col-12 mb-4">
      <h4 className="fw-bold text-white">
        Delivery {state.id}
      </h4>
      <div className="col-12 mb-5">
        <div className="progress">
          { state.status !== 'ready' ? (<div
            className={ state.status === 'active' ? 'progress-bar bg-success progress-bar-striped progress-bar-animated' : 'progress-bar bg-success' }
            role="progressbar"
            style={{width: "50%"}}>
          </div>) : ''}
          { ['collected', 'completed'].includes(state.status) ? (<div
            className={ state.status === 'collected' ? 'progress-bar bg-success progress-bar-striped progress-bar-animated': 'progress-bar bg-success' }
            role="progressbar"
            style={{width: "50%"}}>
          </div>) : ''}
        </div>
      </div>
    </div>
    <div className="col-3">
      <div className="card">
        <div className="card-header">
          Start delivery
        </div>
        <form className="card-body" onSubmit={submit.bind(null, START_DELIVERY)}>
          <button className="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
    <div className="col-3">
      <div className="card">
        <div className="card-header">
          Increase budget
        </div>
        <form className="card-body" onSubmit={submit.bind(null, INCREASE_BUDGET)}>
          <div className="mb-3">
              <input type="number" name="budget" className="form-control" placeholder="Budget..."/>
          </div>
          <button className="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
    <div className="col-3">
      <div className="card">
        <div className="card-header">
          Pickup products
        </div>
        <form className="card-body" onSubmit={submit.bind(null, PICKUP_PRODUCTS)}>
         <div className="mb-3">
            <input type="number" name="quantity" className="form-control" placeholder="Quantity..."/>
          </div>
          <div className="mb-3">
            <input type="number" name="purchase_price" className="form-control" placeholder="Purchase price..."/>
          </div>
          <button className="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
    <div className="col-3">
      <div className="card">
        <div className="card-header">
          Deliver products
        </div>
        <form className="card-body" onSubmit={submit.bind(null, DELIVER_PRODUCTS)}>
         <div className="mb-3">
            <input type="number" name="quantity" className="form-control" placeholder="Quantity..."/>
          </div>
          <div className="mb-3">
            <input type="number" name="sell_price" className="form-control" placeholder="Sell price..."/>
          </div>
          <button className="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
    <div className="col-12 mt-4">
      {JSON.stringify(state)}
    </div>
  </div>;
}
