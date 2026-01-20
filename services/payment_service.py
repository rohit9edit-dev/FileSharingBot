# services/payment_service.py

import os
from datetime import datetime

from config import PAYMENTS_ENABLED, UPI_ID, PAYEE_NAME, PAYMENT_QR_PATH
from services.subscription_service import activate_plan


# =========================================================
# PAYMENT LOGIC
# =========================================================

async def get_payment_info() -> dict:
    """
    Return QR and UPI details for user to pay
    """
    if not PAYMENTS_ENABLED:
        return {"enabled": False}

    return {
        "enabled": True,
        "upi_id": UPI_ID,
        "payee_name": PAYEE_NAME,
        "qr_path": PAYMENT_QR_PATH
    }


async def confirm_payment(user_id: int, plan_name: str, amount: float, tx_id: str) -> dict:
    """
    Confirm payment (manual / automated) and activate plan
    tx_id = transaction ID from user or payment gateway
    """
    if not PAYMENTS_ENABLED:
        raise ValueError("Payments are not enabled")

    # TODO: Integrate actual payment verification if using a gateway
    # For now, assume user sent valid payment

    # Activate the plan
    plan_data = await activate_plan(user_id, plan_name)

    # Record payment in DB (optional)
    payment_record = {
        "user_id": user_id,
        "plan": plan_name,
        "amount": amount,
        "tx_id": tx_id,
        "paid_at": datetime.utcnow()
    }

    # Here you can save payment_record in a collection e.g., payments
    # await save_payment_record(payment_record)

    return plan_data
