import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .farming_pools.alpaca_finance_api import AlpacaFinanceApi

from .config import (
  FRONTEND_URL,
  ALPACA_FINANCE_URL,
)

logger.log(logging.INFO, "allowing origin %s", FRONTEND_URL)

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=[FRONTEND_URL],
  allow_methods=["*"],
  allow_headers=["*"],
)

farming_pool = AlpacaFinanceApi(ALPACA_FINANCE_URL)

from .routes import router
app.include_router(router)
