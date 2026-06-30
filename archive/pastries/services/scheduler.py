from services.automation import run_daily_job
from services.audit import log_action

def run_daily_system(students, payments):
    result = run_daily_job(students, payments)

    log_action("DAILY_RUN", "SYSTEM", "ALL")

    return result
