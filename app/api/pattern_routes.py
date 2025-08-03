from fastapi import APIRouter, Depends, Query, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from datetime import date
import os
from app.database.session import get_db
from app.schemas.pattern import PatternResponse, PatternRankLookup

router = APIRouter()

def verify_api_key(x_api_key: str = Header(...)):
    expected_key = os.getenv("API_KEY")
    if x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Unauthorized access: Invalid API key")

@router.get("/patterns/latest", response_model=List[PatternResponse], dependencies=[Depends(verify_api_key)])
async def get_latest_patterns(
    page: int = Query(1, gt=0),
    limit: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    query = text("""
        SELECT symbol, date, open, high, low, close, volume, prev_close, avg_price, pattern_value, matched_patterns
        FROM common_stock_data
        WHERE pattern_value IS NOT NULL
        ORDER BY date DESC
        LIMIT :limit OFFSET :offset
    """)
    try:
        result = db.execute(query, {"limit": limit, "offset": offset})
        return [dict(row._mapping) for row in result.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/patterns/search", response_model=List[PatternResponse], dependencies=[Depends(verify_api_key)])
async def search_patterns(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    pattern_value: Optional[int] = Query(None),
    symbol: Optional[str] = Query(None),
    page: int = Query(1, gt=0),
    limit: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    clauses = ["pattern_value IS NOT NULL"]
    params = {"limit": limit, "offset": offset}

    if symbol:
        clauses.append("symbol = :symbol")
        params["symbol"] = symbol
    if pattern_value is not None:
        clauses.append("(pattern_value & :pattern_value) = :pattern_value")
        params["pattern_value"] = pattern_value
    if start_date:
        clauses.append("date >= :start_date")
        params["start_date"] = start_date
    if end_date:
        clauses.append("date <= :end_date")
        params["end_date"] = end_date

    query = f"""
        SELECT symbol, date, open, high, low, close, volume, prev_close, avg_price, pattern_value, matched_patterns
        FROM common_stock_data
        WHERE {" AND ".join(clauses)}
        ORDER BY date DESC
        LIMIT :limit OFFSET :offset
    """
    try:
        result = db.execute(text(query), params)
        return [dict(row._mapping) for row in result.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while filtering patterns: {str(e)}")

@router.get("/pattern-rank", response_model=List[PatternRankLookup], dependencies=[Depends(verify_api_key)])
async def get_pattern_rank_lookup(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM pattern_rank_lookup ORDER BY bit_position ASC"))
        return [dict(row._mapping) for row in result.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pattern ranks: {str(e)}")

@router.get("/stock/{symbol}", response_model=List[PatternResponse], dependencies=[Depends(verify_api_key)])
async def get_stock_data_by_symbol(
    symbol: str,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    table_name = f"stock_{symbol.lower()}"
    clauses = ["TRUE"]
    params = {}

    if start_date:
        clauses.append("date >= :start_date")
        params["start_date"] = start_date
    if end_date:
        clauses.append("date <= :end_date")
        params["end_date"] = end_date

    query = f"""
        SELECT symbol, date, open, high, low, close, volume, prev_close, avg_price, pattern_value, matched_patterns
        FROM {table_name}
        WHERE {" AND ".join(clauses)}
        ORDER BY date DESC
    """
    try:
        result = db.execute(text(query), params)
        return [dict(row._mapping) for row in result.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from `{table_name}`: {str(e)}")
