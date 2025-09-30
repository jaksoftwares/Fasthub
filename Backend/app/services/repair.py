from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.repair import RepairRequest
from app.schemas.repair import RepairRequestCreate, RepairRequestUpdate

class RepairService:
    @staticmethod
    def create_repair_request(db: Session, repair: RepairRequestCreate) -> RepairRequest:
        db_repair = RepairRequest(**repair.model_dump())
        db.add(db_repair)
        db.commit()
        db.refresh(db_repair)
        return db_repair
    
    @staticmethod
    def get_repair_request(db: Session, repair_id: int) -> Optional[RepairRequest]:
        return db.query(RepairRequest).filter(RepairRequest.id == repair_id).first()
    
    @staticmethod
    def get_repair_requests(db: Session, skip: int = 0, limit: int = 100, 
                           status: Optional[str] = None, urgency: Optional[str] = None) -> List[RepairRequest]:
        query = db.query(RepairRequest)
        
        if status:
            query = query.filter(RepairRequest.status == status)
        if urgency:
            query = query.filter(RepairRequest.urgency == urgency)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_repair_request(db: Session, repair_id: int, 
                             repair_update: RepairRequestUpdate) -> Optional[RepairRequest]:
        db_repair = RepairService.get_repair_request(db, repair_id)
        if not db_repair:
            return None
        
        update_data = repair_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_repair, field, value)
        
        db.commit()
        db.refresh(db_repair)
        return db_repair
    
    @staticmethod
    def delete_repair_request(db: Session, repair_id: int) -> bool:
        db_repair = RepairService.get_repair_request(db, repair_id)
        if not db_repair:
            return False
        
        db.delete(db_repair)
        db.commit()
        return True