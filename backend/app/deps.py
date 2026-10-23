from typing import Annotated

import httpx
from fastapi import Depends, Request


def get_http(request: Request) -> httpx.AsyncClient:
    return request.app.state.http

HttpClient = Annotated[httpx.AsyncClient, Depends(get_http)]