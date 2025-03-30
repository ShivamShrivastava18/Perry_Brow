from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.sync_api import sync_playwright

app = FastAPI()

class Command(BaseModel):
    action: str
    url: str = None
    query: str = None

@app.post("/interact")
def interact(command: Command):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            if command.action == "open":
                if not command.url:
                    raise HTTPException(status_code=400, detail="URL is required for 'open' action")
                page.goto(command.url)
            
            elif command.action == "search":
                if not command.query:
                    raise HTTPException(status_code=400, detail="Query is required for 'search' action")
                page.fill("input[name='q']", command.query)
                page.press("input[name='q']", "Enter")
            
            else:
                raise HTTPException(status_code=400, detail="Unsupported action")
            
            return {"status": "success", "action": command.action}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
