from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud, schemas

router = APIRouter(prefix="", tags=["scraped"])  # root-level routes per examples

@router.post("/import/scraped", response_model=list[schemas.ScrapedResourceRead])
def import_scraped(items: list[schemas.ScrapedResourceIn], db: Session = Depends(get_db)):
    return crud.insert_scraped(db, items)

@router.get("/scrapedresources", response_model=list[schemas.ScrapedResourceRead])
def list_scraped(limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_scraped(db, limit=limit)
