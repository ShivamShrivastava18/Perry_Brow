from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from playwright.sync_api import sync_playwright

extract_router = APIRouter()

class ExtractRequest(BaseModel):
    url: str
    selector: str

@extract_router.post("/extract")
def extract_data(request: ExtractRequest):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(request.url)
            elements = page.query_selector_all(request.selector)
            data = [element.inner_text() for element in elements]
            browser.close()
            return {"url": request.url, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
