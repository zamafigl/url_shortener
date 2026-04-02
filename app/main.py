from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session
from .db import Base, SessionLocal, engine
from .models import Link
from .utils import generate_short_id
from .schemas import ShortenRequest, ShortenResponse, LinkResponse


app = FastAPI()

Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
RESERVED_CODES = {"health", "shorten", "docs", "openapi.json", "redoc", "links"}



@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )
@app.post("/shorten", response_model=ShortenResponse)
async def shorten_url(payload: ShortenRequest, request: Request):
    db: Session = SessionLocal()

    try:
        short_code = generate_short_id()

        while (
            db.query(Link).filter(Link.short_code == short_code).first()
            or short_code in RESERVED_CODES
        ):
            short_code = generate_short_id()

        new_link = Link(
            original_url=str(payload.url),
            short_code=short_code
        )

        db.add(new_link)
        db.commit()
        db.refresh(new_link)

        short_url = str(request.base_url) + short_code

        return ShortenResponse(
            original_url=new_link.original_url,
            short_code=new_link.short_code,
            short_url=short_url
        )
    finally:
        db.close()
@app.get("/links", response_model=list[LinkResponse])
async def get_links():
    db: Session = SessionLocal()

    try:
        links = db.query(Link).order_by(Link.id.desc()).all()
        return links
    finally:
        db.close()

@app.get("/health")
async def health_check():
    return {"status": "ok"}
@app.get("/links-page")
async def links_page(request: Request):
    db: Session = SessionLocal()

    try:
        links = db.query(Link).order_by(Link.id.desc()).all()
        return templates.TemplateResponse(
            request=request,
            name="links.html",
            context={"request": request, "links": links}
        )
    finally:
        db.close()
@app.get("/{code}")
async def redirect_to_url(code: str):
    db: Session = SessionLocal()

    try:
        link = db.query(Link).filter(Link.short_code == code).first()

        if not link:
            raise HTTPException(status_code=404, detail="Short URL not found")

        link.click_count += 1
        db.commit()

        return RedirectResponse(url=link.original_url)
    finally:
        db.close()