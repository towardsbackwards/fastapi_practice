from fastapi import APIRouter, BackgroundTasks, Depends

from auth.base_config import current_user
from .tasks import send_email_report_dashboard

router = APIRouter(prefix="/report")


@router.get("/dashboard")
def get_dashboard_report(background_tasks: BackgroundTasks, user=Depends(current_user)):
    """
    :param background_tasks:
    :param user:
    :return:
    warning - this is a test function which will send 3 emails using different approaches
    """
    send_email_report_dashboard(user.username)  # synchronous (standard) - approx 1400ms
    background_tasks.add_task(send_email_report_dashboard, user.username)  # async - approx 500ms
    send_email_report_dashboard.delay(user.username)  # celery task - approx 600ms
    return {
        "status": 200,
        "data": "Email has been sent",
        "details": None
    }
