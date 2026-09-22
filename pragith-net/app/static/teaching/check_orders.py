"""Reference solution: validate a small fictional orders CSV."""

import csv
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


def inspect_orders(path):
    accepted = []
    rejected = []
    seen = set()
    with Path(path).open(newline="", encoding="utf-8") as source:
        for row_number, row in enumerate(csv.DictReader(source), start=2):
            order_id = row["order_id"].strip()
            reason = ""
            if not order_id:
                reason = "missing order id"
            elif order_id in seen:
                reason = "duplicate order id"
            else:
                try:
                    amount = Decimal(row["amount"])
                    if not amount.is_finite() or amount <= 0:
                        reason = "amount must be positive"
                except InvalidOperation:
                    reason = "invalid amount"
            if reason:
                rejected.append({"row": row_number, "reason": reason})
            else:
                seen.add(order_id)
                accepted.append(amount)
    return {
        "accepted": len(accepted),
        "rejected": rejected,
        "total": str(sum(accepted, Decimal("0.00"))),
    }


if __name__ == "__main__":
    print(json.dumps(inspect_orders(sys.argv[1]), indent=2))
