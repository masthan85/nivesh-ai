from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.goal import Goal
from app.schemas.portfolio import GoalCreate, GoalUpdate
from app.utils.auth import get_current_user
from app.services.tax_calculator import project_goal, required_sip

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("/")
def get_goals(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goals = db.query(Goal).filter(Goal.user_id == user.id).all()
    result = []
    for g in goals:
        proj     = project_goal(g.saved, g.monthly, g.years, g.risk)
        progress = min(100, g.saved / g.target * 100) if g.target else 0
        req_sip  = required_sip(g.target, g.saved, g.years, g.risk)
        result.append({
            "id":          g.id,
            "name":        g.name,
            "icon":        g.icon,
            "target":      g.target,
            "saved":       g.saved,
            "monthly":     g.monthly,
            "years":       g.years,
            "risk":        g.risk,
            "color":       g.color,
            "progress_pct":round(progress, 1),
            "projected":   proj["projected"],
            "on_track":    proj["projected"] >= g.target,
            "gap":         round(max(0, g.target - proj["projected"]), 2),
            "required_sip":req_sip,
        })
    return result


@router.post("/", status_code=201)
def create_goal(data: GoalCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    g = Goal(user_id=user.id, **data.dict())
    db.add(g)
    db.commit()
    db.refresh(g)
    return g


@router.put("/{goal_id}")
def update_goal(goal_id: int, data: GoalUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    g = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user.id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Goal not found")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(g, k, v)
    db.commit()
    db.refresh(g)
    return g


@router.delete("/{goal_id}")
def delete_goal(goal_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    g = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user.id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(g)
    db.commit()
    return {"ok": True}
