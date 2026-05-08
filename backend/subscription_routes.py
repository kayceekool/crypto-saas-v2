from fastapi import APIRouter

router = APIRouter()

@router.post("/subscribe")
def subscribe(user: str, plan: str):

    return {
        "status": "pending",
        "plan": plan
    }