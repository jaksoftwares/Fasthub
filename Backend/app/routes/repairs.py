from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config import get_db
from app.schemas.repair import RepairRequest, RepairRequestCreate, RepairRequestUpdate
from app.services.repair import RepairService

router = APIRouter(prefix="/repairs", tags=["repairs"])

@router.post("/", response_model=RepairRequest)
def create_repair_request(repair: RepairRequestCreate, db: Session = Depends(get_db)):
    return RepairService.create_repair_request(db, repair)

@router.get("/", response_model=List[RepairRequest])
def get_repair_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    urgency: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return RepairService.get_repair_requests(db, skip=skip, limit=limit, status=status, urgency=urgency)

@router.get("/{repair_id}", response_model=RepairRequest)
def get_repair_request(repair_id: int, db: Session = Depends(get_db)):
    repair = RepairService.get_repair_request(db, repair_id)
    if not repair:
        raise HTTPException(status_code=404, detail="Repair request not found")
    return repair

@router.put("/{repair_id}", response_model=RepairRequest)
def update_repair_request(repair_id: int, repair_update: RepairRequestUpdate, db: Session = Depends(get_db)):
    repair = RepairService.update_repair_request(db, repair_id, repair_update)
    if not repair:
        raise HTTPException(status_code=404, detail="Repair request not found")
    return repair

@router.delete("/{repair_id}")
def delete_repair_request(repair_id: int, db: Session = Depends(get_db)):
    success = RepairService.delete_repair_request(db, repair_id)
    if not success:
        raise HTTPException(status_code=404, detail="Repair request not found")
    return {"message": "Repair request deleted successfully"}