from fastapi import APIRouter, Request

from app import farming_pool
from app.simulation.utils import simulate_position


POOL_ID = 'pool_id'
USD_TO_INVEST = 'usd_to_invest'
DURATION_DAYS = 'duration_days'

GET = 'GET'
POST = 'POST'


router = APIRouter()

@router.get("/pools")
async def get_pools():
    return farming_pool.get_pools()

@router.post("/simulate")
async def simulate(request: Request):
    data = await request.json()

    pool_id = data[POOL_ID]
    duration_days = data[DURATION_DAYS]

    pool = farming_pool.get_pool_by_id(pool_id)

    trading_fee = pool.trading_fee
    borrow_rate_one = pool.borrow_rate_one
    borrow_rate_two = pool.borrow_rate_two

    result = simulate_position(duration_days, trading_fee, borrow_rate_one, borrow_rate_two)
    
    return result
