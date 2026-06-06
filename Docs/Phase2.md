# PHASE 2 – SMART RESERVE CORE ENGINE

## Objective

Build the first working version of Smart Reserve.

The goal is to maintain a reserve balance and allow payments during simulated bank outages.

No AI.

No outage prediction.

No risk scoring.

Only reserve management.

---

# Core Features

1. Reserve Settings
2. Reserve Balance Tracking
3. Auto Topup
4. Refill Queue
5. Payment Routing
6. Simulated Outage Handling

---

# Repository Structure

phase2/

backend/

frontend/

database/

tests/

docs/

---

# Database Tables

## reserve_settings

id

user_id

target_balance

threshold_balance

auto_topup

created_at

---

## reserve_balance

id

user_id

current_balance

updated_at

---

## reserve_transactions

id

user_id

amount

transaction_type

status

created_at

---

## refill_queue

id

user_id

amount

status

retry_count

created_at

---

# Backend

Framework:

FastAPI

---

# APIs

## Reserve Settings

GET /api/reserve/settings

POST /api/reserve/settings

PUT /api/reserve/settings

---

## Reserve Balance

GET /api/reserve/balance

POST /api/reserve/topup

---

## Payment

POST /api/payment

Request:

{
"amount":200
}

---

## Queue

GET /api/refill-queue

POST /api/refill-queue/process

---

# Business Logic

## Payment Router

If reserve balance >= payment amount

Use reserve.

Else

Use bank account.

---

## Auto Topup

gap = target_balance - current_balance

If gap > 0

Create topup request.

---

## Outage Mode

Create outage simulation toggle.

Bank Status:

HEALTHY

OUTAGE

---

If OUTAGE

Topups must be queued.

Payments continue using reserve.

---

# Frontend

Dashboard must show:

Reserve Balance

Target Balance

Threshold

Required Topup

Bank Status

Queue Count

Transaction History

---

# Sample Data

Generate:

10 users

Reserve balances

Transactions

Pending queue records

---

# Testing

Test:

Payment Success

Payment Failure

Reserve Depletion

Queue Creation

Queue Processing

Outage Handling

---

# Success Criteria

Phase 2 is successful when:

1. User can configure reserve.
2. User can spend from reserve.
3. Outage simulation works.
4. Refill queue works.
5. Auto topup works.
6. Dashboard reflects live state.

No AI.

No outage prediction.

No notifications.

No risk scoring.
