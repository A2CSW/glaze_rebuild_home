from services.invoice_engine import generate_monthly_invoices, load_invoices
from services.payment_matching import match_payments_to_invoices
from services.family_alerts import generate_family_alerts
from services.metrics import calculate_kpis

def run_daily_job(students, payments):
    """
    Simulates a scheduled daily backend job
    """

    invoices = load_invoices()

    invoices = match_payments_to_invoices(invoices, payments)

    alerts = generate_family_alerts(invoices)

    kpis = calculate_kpis(invoices, payments)

    return {
        "invoices": invoices,
        "alerts": alerts,
        "kpis": kpis
    }
