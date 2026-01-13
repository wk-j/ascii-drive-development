# ASCII Driven Development (ADD)

A methodology for software development using plain-text ASCII diagrams and documentation throughout the entire development lifecycle.

```
    +------------------------------------------------------------------+
    |                  ASCII DRIVEN DEVELOPMENT                        |
    |                                                                  |
    |   "If you can't express it in ASCII, you don't understand it"   |
    +------------------------------------------------------------------+
```

## Table of Contents

1. [Introduction](#introduction)
2. [The Software Development Cycle](#the-software-development-cycle)
3. [Phase 1: Requirements & Planning](#phase-1-requirements--planning)
4. [Phase 2: Design](#phase-2-design)
5. [Phase 3: Implementation](#phase-3-implementation)
6. [Phase 4: Testing](#phase-4-testing)
7. [Phase 5: Deployment & Operations](#phase-5-deployment--operations)
8. [Phase 6: Maintenance & Evolution](#phase-6-maintenance--evolution)
9. [ASCII Diagram Reference](#ascii-diagram-reference)

---

## Introduction

ASCII Driven Development (ADD) is a methodology that emphasizes using plain-text ASCII art and diagrams as the primary means of documenting, designing, and communicating software systems.

### Why ASCII?

```
+-------------------+     +-------------------+     +-------------------+
|   UNIVERSAL       |     |   VERSION         |     |   LIGHTWEIGHT     |
|                   |     |   CONTROL         |     |                   |
| - Works anywhere  |     | - Git-friendly    |     | - No special      |
| - No special      |     | - Diff-able       |     |   tools needed    |
|   software        |     | - Merge-able      |     | - Fast to create  |
| - Copy/paste      |     | - History tracked |     | - Easy to modify  |
+-------------------+     +-------------------+     +-------------------+
         |                        |                        |
         +------------------------+------------------------+
                                  |
                                  v
                    +---------------------------+
                    |   BETTER COMMUNICATION    |
                    |                           |
                    | - Clear mental models     |
                    | - Shared understanding    |
                    | - Documentation as code   |
                    +---------------------------+
```

---

## The Software Development Cycle

```
                            +-------------------+
                            |   REQUIREMENTS    |
                            |    & PLANNING     |
                            +--------+----------+
                                     |
                                     v
+-------------------+       +-------------------+       +-------------------+
|   MAINTENANCE     |       |                   |       |                   |
|   & EVOLUTION     |<------+      DESIGN       +------>|  IMPLEMENTATION   |
+--------+----------+       |                   |       +--------+----------+
         ^                  +-------------------+                |
         |                                                       |
         |                                                       v
         |                  +-------------------+       +-------------------+
         |                  |    DEPLOYMENT     |       |                   |
         +------------------+   & OPERATIONS    |<------+     TESTING       |
                            +-------------------+       +-------------------+


    Legend:
    ------> : Primary flow
    <------ : Feedback loop
```

### Iterative Nature

```
    Iteration 1          Iteration 2          Iteration 3

    +-------+            +-------+            +-------+
    | Plan  |            | Plan  |            | Plan  |
    +---+---+            +---+---+            +---+---+
        |                    |                    |
        v                    v                    v
    +-------+            +-------+            +-------+
    | Build |            | Build |            | Build |
    +---+---+            +---+---+            +---+---+
        |                    |                    |
        v                    v                    v
    +-------+            +-------+            +-------+
    | Test  |            | Test  |            | Test  |
    +---+---+            +---+---+            +---+---+
        |                    |                    |
        v                    v                    v
    [MVP v0.1]           [Beta v0.5]          [Release v1.0]
```

---

## Phase 1: Requirements & Planning

### Purpose

Capture and organize what the system needs to do before writing any code.

### ASCII Artifacts

#### User Story Map

```
+===========================================================================+
|                           USER STORY MAP                                  |
+===========================================================================+
|                                                                           |
|  ACTIVITIES:   [ Browse ]    [ Purchase ]    [ Manage Account ]          |
|                    |              |                  |                    |
+--------------------|--------------|------------------|--------------------+
|                    |              |                  |                    |
|  USER TASKS:       |              |                  |                    |
|                    v              v                  v                    |
|              +-----------+  +-----------+     +-----------+               |
|              | Search    |  | Add to    |     | View      |               |
|              | Products  |  | Cart      |     | Profile   |               |
|              +-----------+  +-----------+     +-----------+               |
|                    |              |                  |                    |
|              +-----------+  +-----------+     +-----------+               |
|              | Filter    |  | Checkout  |     | Edit      |               |
|              | Results   |  |           |     | Settings  |               |
|              +-----------+  +-----------+     +-----------+               |
|                    |              |                  |                    |
|              +-----------+  +-----------+     +-----------+               |
|              | View      |  | Pay       |     | View      |               |
|              | Details   |  |           |     | Orders    |               |
|              +-----------+  +-----------+     +-----------+               |
|                                                                           |
+===========================================================================+
|  RELEASE 1:  [Search] [View Details] [Add to Cart] [Checkout]            |
|  RELEASE 2:  [Filter] [Pay] [View Profile]                               |
|  RELEASE 3:  [Edit Settings] [View Orders]                               |
+===========================================================================+
```

#### Requirements Matrix

```
+------+---------------------------+----------+----------+--------+
| ID   | Requirement               | Priority | Estimate | Status |
+------+---------------------------+----------+----------+--------+
| R001 | User authentication       | HIGH     | 3 days   | [TODO] |
| R002 | Product catalog           | HIGH     | 5 days   | [TODO] |
| R003 | Shopping cart             | HIGH     | 3 days   | [TODO] |
| R004 | Payment processing        | HIGH     | 5 days   | [TODO] |
| R005 | Order history             | MEDIUM   | 2 days   | [TODO] |
| R006 | Email notifications       | MEDIUM   | 2 days   | [TODO] |
| R007 | Admin dashboard           | LOW      | 5 days   | [TODO] |
+------+---------------------------+----------+----------+--------+
```

#### Sprint Planning Board

```
+==================+==================+==================+==================+
|     BACKLOG      |    TO DO         |   IN PROGRESS    |      DONE        |
+==================+==================+==================+==================+
|                  |                  |                  |                  |
| [ ] R007 Admin   | [ ] R005 Order   | [~] R002 Product | [x] R001 Auth    |
|     dashboard    |     history      |     catalog      |                  |
|                  |                  |                  |                  |
| [ ] R006 Email   | [ ] R004 Payment |                  | [x] R003 Cart    |
|     notifs       |                  |                  |                  |
|                  |                  |                  |                  |
+------------------+------------------+------------------+------------------+
| Items: 2         | Items: 2         | Items: 1         | Items: 2         |
+==================+==================+==================+==================+
```

---

## Phase 2: Design

### Purpose

Define the system architecture, data models, and component interactions.

### ASCII Artifacts

#### System Architecture Diagram

```
+===========================================================================+
|                         SYSTEM ARCHITECTURE                               |
+===========================================================================+

                              +-------------+
                              |   CLIENT    |
                              | (Browser/   |
                              |  Mobile)    |
                              +------+------+
                                     |
                                     | HTTPS
                                     v
                        +------------------------+
                        |     LOAD BALANCER      |
                        |      (nginx/HAProxy)   |
                        +------------------------+
                           /         |         \
                          /          |          \
                         v           v           v
                   +--------+   +--------+   +--------+
                   | App    |   | App    |   | App    |
                   | Server |   | Server |   | Server |
                   | (1)    |   | (2)    |   | (3)    |
                   +---+----+   +---+----+   +---+----+
                       \           |           /
                        \          |          /
                         v         v         v
              +-------------+-------------+-------------+
              |             |             |             |
        +-----+-----+ +-----+-----+ +-----+-----+ +-----+-----+
        |  Primary  | |  Replica  | |   Cache   | |  Message  |
        |    DB     | |    DB     | |  (Redis)  | |  Queue    |
        | (Postgres)| | (Postgres)| |           | | (RabbitMQ)|
        +-----------+ +-----------+ +-----------+ +-----------+
```

#### Component Diagram

```
+------------------------------------------------------------------+
|                        APPLICATION LAYER                          |
+------------------------------------------------------------------+
|                                                                   |
|  +------------------+  +------------------+  +------------------+ |
|  |   Auth Module    |  |  Product Module  |  |   Order Module   | |
|  |                  |  |                  |  |                  | |
|  | - login()        |  | - list()         |  | - create()       | |
|  | - logout()       |  | - search()       |  | - cancel()       | |
|  | - register()     |  | - getDetails()   |  | - getStatus()    | |
|  | - resetPassword()|  | - updateStock()  |  | - listByUser()   | |
|  +--------+---------+  +--------+---------+  +--------+---------+ |
|           |                     |                     |           |
+-----------+---------------------+---------------------+-----------+
            |                     |                     |
            v                     v                     v
+------------------------------------------------------------------+
|                        SERVICE LAYER                              |
+------------------------------------------------------------------+
|                                                                   |
|  +------------------+  +------------------+  +------------------+ |
|  | AuthService      |  | ProductService   |  | OrderService     | |
|  +------------------+  +------------------+  +------------------+ |
|  | PaymentService   |  | NotificationSvc  |  | InventoryService | |
|  +------------------+  +------------------+  +------------------+ |
|                                                                   |
+------------------------------------------------------------------+
            |                     |                     |
            v                     v                     v
+------------------------------------------------------------------+
|                        DATA ACCESS LAYER                          |
+------------------------------------------------------------------+
|                                                                   |
|  +------------------+  +------------------+  +------------------+ |
|  | UserRepository   |  | ProductRepository|  | OrderRepository  | |
|  +------------------+  +------------------+  +------------------+ |
|                                                                   |
+------------------------------------------------------------------+
```

#### Database Schema (ERD)

```
+------------------+       +------------------+       +------------------+
|      USERS       |       |     PRODUCTS     |       |     ORDERS       |
+------------------+       +------------------+       +------------------+
| PK id            |       | PK id            |       | PK id            |
|    email         |       |    name          |       | FK user_id       |----+
|    password_hash |       |    description   |       |    status        |    |
|    first_name    |       |    price         |       |    total_amount  |    |
|    last_name     |       |    stock_qty     |       |    created_at    |    |
|    created_at    |       | FK category_id   |--+    |    updated_at    |    |
+--------+---------+       +--------+---------+  |    +--------+---------+    |
         |                          |            |             |              |
         |                          |            |             |              |
         |    +------------------+  |            |             |              |
         |    |   ORDER_ITEMS    |  |            |             |              |
         |    +------------------+  |            |             |              |
         |    | PK id            |  |            |             |              |
         |    | FK order_id      |--+------------+-------------+              |
         |    | FK product_id    |--+                                         |
         |    |    quantity      |                                            |
         |    |    unit_price    |               +------------------+         |
         |    +------------------+               |    CATEGORIES    |         |
         |                                       +------------------+         |
         |                                       | PK id            |---------+
         +---------------------------------------+    name          |
                                                 |    parent_id     |
                                                 +------------------+

    Legend:
    PK = Primary Key
    FK = Foreign Key
    --- = Relationship
```

#### Sequence Diagram

```
    User           Frontend        API Gateway      Auth Service      Database
      |               |                |                |                |
      | 1. Login      |                |                |                |
      |-------------->|                |                |                |
      |               | 2. POST /login |                |                |
      |               |--------------->|                |                |
      |               |                | 3. Validate    |                |
      |               |                |--------------->|                |
      |               |                |                | 4. Query user  |
      |               |                |                |--------------->|
      |               |                |                |                |
      |               |                |                | 5. User data   |
      |               |                |                |<---------------|
      |               |                |                |                |
      |               |                | 6. JWT token   |                |
      |               |                |<---------------|                |
      |               | 7. 200 OK      |                |                |
      |               |    + token     |                |                |
      |               |<---------------|                |                |
      | 8. Logged in  |                |                |                |
      |<--------------|                |                |                |
      |               |                |                |                |
```

#### State Machine Diagram

```
                              ORDER STATE MACHINE

                                  +--------+
                                  | DRAFT  |
                                  +---+----+
                                      |
                                      | submit()
                                      v
                                 +---------+
                      +--------->| PENDING |<---------+
                      |          +----+----+          |
                      |               |               |
                      |               | payment       |
               retry()|               | received      | payment
                      |               v               | failed
                      |          +---------+          |
                      +----------+  PAID   +----------+
                                 +----+----+
                                      |
                                      | ship()
                                      v
                                 +---------+
                      +--------->| SHIPPED |
                      |          +----+----+
                      |               |
               update |               | deliver()
              tracking|               v
                      |          +-----------+
                      +----------+ DELIVERED |
                                 +-----------+
                                      |
                                      | (after 30 days)
                                      v
                                 +-----------+
                                 | COMPLETED |
                                 +-----------+

    CANCELLATION (from PENDING, PAID, SHIPPED):

        [ANY STATE] --cancel()--> [CANCELLED]
```

---

## Phase 3: Implementation

### Purpose

Write code, following the designs and meeting the requirements.

### ASCII Artifacts

#### Code Structure / Project Layout

```
project-root/
|
+-- src/
|   +-- controllers/
|   |   +-- auth.controller.ts
|   |   +-- product.controller.ts
|   |   +-- order.controller.ts
|   |
|   +-- services/
|   |   +-- auth.service.ts
|   |   +-- product.service.ts
|   |   +-- order.service.ts
|   |   +-- payment.service.ts
|   |
|   +-- models/
|   |   +-- user.model.ts
|   |   +-- product.model.ts
|   |   +-- order.model.ts
|   |
|   +-- repositories/
|   |   +-- user.repository.ts
|   |   +-- product.repository.ts
|   |   +-- order.repository.ts
|   |
|   +-- middleware/
|   |   +-- auth.middleware.ts
|   |   +-- error.middleware.ts
|   |   +-- logging.middleware.ts
|   |
|   +-- utils/
|   |   +-- validators.ts
|   |   +-- helpers.ts
|   |
|   +-- config/
|   |   +-- database.ts
|   |   +-- app.ts
|   |
|   +-- app.ts
|   +-- server.ts
|
+-- tests/
|   +-- unit/
|   +-- integration/
|   +-- e2e/
|
+-- docs/
+-- scripts/
+-- package.json
+-- tsconfig.json
+-- README.md
```

#### API Endpoint Documentation

```
+==========================================================================+
|                           REST API ENDPOINTS                             |
+==========================================================================+

AUTHENTICATION
--------------
POST   /api/v1/auth/register     Register new user
POST   /api/v1/auth/login        User login
POST   /api/v1/auth/logout       User logout
POST   /api/v1/auth/refresh      Refresh JWT token
POST   /api/v1/auth/reset-password   Reset password

PRODUCTS
--------
GET    /api/v1/products          List all products
GET    /api/v1/products/:id      Get product by ID
POST   /api/v1/products          Create product (admin)
PUT    /api/v1/products/:id      Update product (admin)
DELETE /api/v1/products/:id      Delete product (admin)
GET    /api/v1/products/search   Search products

ORDERS
------
GET    /api/v1/orders            List user's orders
GET    /api/v1/orders/:id        Get order details
POST   /api/v1/orders            Create new order
PUT    /api/v1/orders/:id        Update order
DELETE /api/v1/orders/:id        Cancel order

USERS
-----
GET    /api/v1/users/me          Get current user profile
PUT    /api/v1/users/me          Update profile
GET    /api/v1/users             List users (admin)
GET    /api/v1/users/:id         Get user by ID (admin)

+==========================================================================+
| HTTP Status Codes:                                                       |
| 200 OK | 201 Created | 204 No Content | 400 Bad Request                 |
| 401 Unauthorized | 403 Forbidden | 404 Not Found | 500 Server Error     |
+==========================================================================+
```

#### Git Branching Strategy

```
main          *-----------*-----------*-----------*-----------*
               \         / \         /             \         /
                \       /   \       /               \       /
release/1.0      *-----*     \     /                 \     /
                  \           \   /                   \   /
                   \           \ /                     \ /
develop             *---*---*---*---*---*---*---*---*---*
                     \     / \     /     \         /
                      \   /   \   /       \       /
feature/auth           *-*     \ /         \     /
                                *           \   /
feature/cart                   / \           \ /
                              *---*           *
                                             / \
feature/checkout                            *---*

Legend:
    * = commit
    main = production-ready code
    develop = integration branch
    release/* = release preparation
    feature/* = feature development
```

#### Code Review Checklist

```
+===========================================================================+
|                        CODE REVIEW CHECKLIST                              |
+===========================================================================+

FUNCTIONALITY
[ ] Code implements the required functionality
[ ] Edge cases are handled
[ ] Error handling is appropriate
[ ] No obvious bugs

CODE QUALITY
[ ] Follows project coding standards
[ ] No code duplication (DRY)
[ ] Functions are small and focused
[ ] Variable/function names are clear
[ ] No dead code or commented-out code

SECURITY
[ ] Input validation is present
[ ] No SQL injection vulnerabilities
[ ] No XSS vulnerabilities
[ ] Sensitive data is not logged
[ ] Authentication/authorization checked

TESTING
[ ] Unit tests cover new code
[ ] Tests are meaningful (not just for coverage)
[ ] Edge cases are tested
[ ] Tests pass locally

DOCUMENTATION
[ ] Public APIs are documented
[ ] Complex logic has comments
[ ] README updated if needed

PERFORMANCE
[ ] No obvious performance issues
[ ] Database queries are optimized
[ ] No N+1 query problems

+===========================================================================+
```

---

## Phase 4: Testing

### Purpose

Verify the system works correctly and meets requirements.

### ASCII Artifacts

#### Test Pyramid

```
                           /\
                          /  \
                         / E2E\              Fewer, slower, more expensive
                        / Tests\
                       /--------\
                      /          \
                     / Integration\
                    /    Tests     \
                   /----------------\
                  /                  \
                 /    Unit Tests      \       More, faster, cheaper
                /______________________\

    +-----------------------------------------------------------------+
    | Layer       | Count | Speed  | Cost    | Scope                  |
    +-----------------------------------------------------------------+
    | E2E         | ~50   | Slow   | High    | Full user journeys     |
    | Integration | ~200  | Medium | Medium  | Component interactions |
    | Unit        | ~1000 | Fast   | Low     | Individual functions   |
    +-----------------------------------------------------------------+
```

#### Test Coverage Report

```
+==========================================================================+
|                         TEST COVERAGE REPORT                             |
+==========================================================================+

Module                  | Statements | Branches | Functions | Lines
------------------------+------------+----------+-----------+-------
src/controllers         |     92.5%  |   88.0%  |    95.0%  | 92.0%
src/services            |     95.0%  |   91.5%  |    97.0%  | 94.5%
src/models              |     88.0%  |   82.0%  |    90.0%  | 87.5%
src/repositories        |     90.5%  |   85.5%  |    92.0%  | 90.0%
src/middleware          |     85.0%  |   78.0%  |    88.0%  | 84.0%
src/utils               |     98.0%  |   95.0%  |   100.0%  | 97.5%
------------------------+------------+----------+-----------+-------
TOTAL                   |     91.5%  |   86.7%  |    93.7%  | 90.9%

Coverage Thresholds:
  [============================  ] 90% target
  [=========================     ] 85% minimum
  [XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX] Current: 91.5%

Status: PASSING
+==========================================================================+
```

#### Test Case Matrix

```
+-------+--------------------------------+----------+--------+--------+
| TC-ID | Test Case Description          | Priority | Status | Result |
+-------+--------------------------------+----------+--------+--------+
| TC001 | User can register with valid   | HIGH     | DONE   | PASS   |
|       | email and password             |          |        |        |
+-------+--------------------------------+----------+--------+--------+
| TC002 | User cannot register with      | HIGH     | DONE   | PASS   |
|       | existing email                 |          |        |        |
+-------+--------------------------------+----------+--------+--------+
| TC003 | User can login with correct    | HIGH     | DONE   | PASS   |
|       | credentials                    |          |        |        |
+-------+--------------------------------+----------+--------+--------+
| TC004 | User cannot login with wrong   | HIGH     | DONE   | PASS   |
|       | password                       |          |        |        |
+-------+--------------------------------+----------+--------+--------+
| TC005 | User can add product to cart   | HIGH     | DONE   | PASS   |
+-------+--------------------------------+----------+--------+--------+
| TC006 | User can checkout with items   | HIGH     | IN     | --     |
|       | in cart                        |          | PROG   |        |
+-------+--------------------------------+----------+--------+--------+
| TC007 | User cannot checkout with      | MEDIUM   | TODO   | --     |
|       | empty cart                     |          |        |        |
+-------+--------------------------------+----------+--------+--------+
| TC008 | Order status updates on        | MEDIUM   | TODO   | --     |
|       | payment confirmation           |          |        |        |
+-------+--------------------------------+----------+--------+--------+

Summary: 5/8 tests passing | 1 in progress | 2 pending
```

#### Bug Report Template

```
+==========================================================================+
|                            BUG REPORT                                    |
+==========================================================================+

BUG ID:        BUG-2024-0042
TITLE:         Payment fails silently when card expires
SEVERITY:      HIGH
PRIORITY:      P1 - Critical
STATUS:        OPEN
REPORTED BY:   qa-team
ASSIGNED TO:   dev-payments

+---------------------------------------------------------------------------+
| DESCRIPTION                                                               |
+---------------------------------------------------------------------------+
| When a user attempts to complete checkout with an expired credit card,    |
| the payment silently fails without displaying an error message to the     |
| user. The order remains in 'PENDING' state indefinitely.                  |
+---------------------------------------------------------------------------+

+---------------------------------------------------------------------------+
| STEPS TO REPRODUCE                                                        |
+---------------------------------------------------------------------------+
| 1. Add items to cart                                                      |
| 2. Proceed to checkout                                                    |
| 3. Enter expired credit card details (exp: 01/2020)                       |
| 4. Click 'Pay Now'                                                        |
| 5. Observe: No error shown, page appears to hang                          |
+---------------------------------------------------------------------------+

+---------------------------------------------------------------------------+
| EXPECTED vs ACTUAL                                                        |
+---------------------------------------------------------------------------+
| EXPECTED: Error message "Card expired. Please use a valid card."          |
| ACTUAL:   No message displayed, payment status unclear                    |
+---------------------------------------------------------------------------+

+---------------------------------------------------------------------------+
| ENVIRONMENT                                                               |
+---------------------------------------------------------------------------+
| Browser: Chrome 120.0.6099.130                                            |
| OS: macOS 14.2                                                            |
| Environment: Staging                                                      |
| API Version: v1.2.3                                                       |
+---------------------------------------------------------------------------+
```

---

## Phase 5: Deployment & Operations

### Purpose

Release software to production and maintain operational health.

### ASCII Artifacts

#### Deployment Pipeline

```
+==========================================================================+
|                        CI/CD PIPELINE                                    |
+==========================================================================+

    +--------+    +--------+    +--------+    +--------+    +--------+
    |  CODE  |--->|  BUILD |--->|  TEST  |--->| DEPLOY |--->|MONITOR |
    | COMMIT |    |        |    |        |    |        |    |        |
    +--------+    +--------+    +--------+    +--------+    +--------+
        |             |             |             |             |
        v             v             v             v             v
    +--------+    +--------+    +--------+    +--------+    +--------+
    | Lint   |    | Compile|    | Unit   |    | Staging|    | Logs   |
    | Format |    | Bundle |    | Integr.|    | Prod   |    | Metrics|
    | Scan   |    | Docker |    | E2E    |    | Rollout|    | Alerts |
    +--------+    +--------+    +--------+    +--------+    +--------+

    GATES:
    [Code]    --> PR Approval Required
    [Build]   --> Must succeed (exit 0)
    [Test]    --> Coverage >= 85%, All tests pass
    [Deploy]  --> Manual approval for production
    [Monitor] --> No critical alerts for 30 min

+==========================================================================+
```

#### Infrastructure Diagram

```
                            CLOUD INFRASTRUCTURE

    +==================================================================+
    |                         VPC (10.0.0.0/16)                        |
    +==================================================================+
    |                                                                   |
    |  +------------------------+    +------------------------+        |
    |  |   PUBLIC SUBNET        |    |   PUBLIC SUBNET        |        |
    |  |   10.0.1.0/24          |    |   10.0.2.0/24          |        |
    |  |   (AZ-a)               |    |   (AZ-b)               |        |
    |  |                        |    |                        |        |
    |  |  +------------------+  |    |  +------------------+  |        |
    |  |  | Load Balancer   |  |    |  | NAT Gateway      |  |        |
    |  |  +------------------+  |    |  +------------------+  |        |
    |  +----------+-------------+    +----------+-------------+        |
    |             |                             |                      |
    |  +----------+-------------+    +----------+-------------+        |
    |  |   PRIVATE SUBNET       |    |   PRIVATE SUBNET       |        |
    |  |   10.0.10.0/24         |    |   10.0.20.0/24         |        |
    |  |   (AZ-a)               |    |   (AZ-b)               |        |
    |  |                        |    |                        |        |
    |  |  +------+  +------+    |    |  +------+  +------+    |        |
    |  |  | App  |  | App  |    |    |  | App  |  | App  |    |        |
    |  |  | (1)  |  | (2)  |    |    |  | (3)  |  | (4)  |    |        |
    |  |  +------+  +------+    |    |  +------+  +------+    |        |
    |  +------------------------+    +------------------------+        |
    |                                                                   |
    |  +------------------------+    +------------------------+        |
    |  |   DATA SUBNET          |    |   DATA SUBNET          |        |
    |  |   10.0.100.0/24        |    |   10.0.200.0/24        |        |
    |  |                        |    |                        |        |
    |  |  +------------------+  |    |  +------------------+  |        |
    |  |  | DB Primary       |  |    |  | DB Replica       |  |        |
    |  |  +------------------+  |    |  +------------------+  |        |
    |  +------------------------+    +------------------------+        |
    |                                                                   |
    +==================================================================+
```

#### Deployment Runbook

```
+==========================================================================+
|                     PRODUCTION DEPLOYMENT RUNBOOK                        |
+==========================================================================+

PRE-DEPLOYMENT CHECKLIST
------------------------
[ ] All tests passing in CI
[ ] Code review approved
[ ] Release notes prepared
[ ] Rollback plan documented
[ ] On-call engineer notified
[ ] Database migrations tested in staging

DEPLOYMENT STEPS
----------------
1. [ ] Announce deployment in #ops channel

2. [ ] Enable maintenance mode (if required)
       $ kubectl apply -f maintenance-mode.yaml

3. [ ] Create database backup
       $ ./scripts/backup-db.sh production

4. [ ] Run database migrations
       $ kubectl exec -it db-pod -- ./migrate.sh

5. [ ] Deploy new version
       $ kubectl set image deployment/app app=myapp:v1.2.3

6. [ ] Monitor rollout
       $ kubectl rollout status deployment/app

7. [ ] Verify health checks
       $ curl https://api.example.com/health

8. [ ] Run smoke tests
       $ ./scripts/smoke-test.sh production

9. [ ] Disable maintenance mode
       $ kubectl delete -f maintenance-mode.yaml

10.[ ] Announce deployment complete

ROLLBACK PROCEDURE
------------------
If issues detected:
    $ kubectl rollout undo deployment/app
    $ ./scripts/restore-db.sh <backup-id>

+==========================================================================+
```

#### Monitoring Dashboard Layout

```
+==========================================================================+
|                        MONITORING DASHBOARD                              |
+==========================================================================+

+-------------------------+  +-------------------------+  +----------------+
|     REQUEST RATE        |  |      ERROR RATE         |  |    UPTIME      |
|                         |  |                         |  |                |
|   1200 req/s   [====]   |  |   0.05%        [=]      |  |   99.97%       |
|                         |  |                         |  |    30d         |
|   ^^^^                  |  |   ---___---            |  |                |
|  /    \    /\           |  |                         |  |  [=========]   |
| /      \  /  \          |  |   Target: < 0.1%       |  |                |
|/        \/    \___      |  |   Status: OK           |  |  Target: 99.9% |
+-------------------------+  +-------------------------+  +----------------+

+-------------------------+  +-------------------------+  +----------------+
|    RESPONSE TIME        |  |      CPU USAGE          |  | MEMORY USAGE   |
|                         |  |                         |  |                |
|   p50:  45ms            |  |   App-1: 42% [====    ] |  |  App-1: 68%    |
|   p95: 120ms            |  |   App-2: 38% [===     ] |  |  App-2: 72%    |
|   p99: 250ms            |  |   App-3: 45% [====    ] |  |  App-3: 65%    |
|                         |  |   App-4: 41% [====    ] |  |  App-4: 70%    |
|   [=====     ] OK       |  |                         |  |                |
+-------------------------+  +-------------------------+  +----------------+

+-----------------------------------------------------------------------+
|                          RECENT ALERTS                                 |
+-----------------------------------------------------------------------+
| [WARN]  10:23  High memory usage on App-2 (>80%)        [RESOLVED]    |
| [INFO]  09:45  Deployment v1.2.3 completed              [CLOSED]      |
| [CRIT]  Yesterday  Database connection pool exhausted   [RESOLVED]    |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
|                        ACTIVE INCIDENTS                               |
+-----------------------------------------------------------------------+
|                        No active incidents                            |
|                             Status: ALL SYSTEMS OPERATIONAL           |
+-----------------------------------------------------------------------+
```

---

## Phase 6: Maintenance & Evolution

### Purpose

Keep the system running smoothly and evolve it to meet changing needs.

### ASCII Artifacts

#### Technical Debt Tracker

```
+==========================================================================+
|                       TECHNICAL DEBT REGISTER                            |
+==========================================================================+

+------+----------------------------------+----------+--------+------------+
| ID   | Description                      | Impact   | Effort | Priority   |
+------+----------------------------------+----------+--------+------------+
| TD01 | Legacy auth system needs         | HIGH     | HIGH   | P1         |
|      | migration to OAuth 2.0           |          |        |            |
+------+----------------------------------+----------+--------+------------+
| TD02 | N+1 queries in order listing     | MEDIUM   | LOW    | P2         |
|      | causing slow page loads          |          |        |            |
+------+----------------------------------+----------+--------+------------+
| TD03 | Missing input validation on      | HIGH     | MEDIUM | P1         |
|      | product import API               |          |        |            |
+------+----------------------------------+----------+--------+------------+
| TD04 | Inconsistent error handling      | LOW      | MEDIUM | P3         |
|      | across services                  |          |        |            |
+------+----------------------------------+----------+--------+------------+
| TD05 | No database connection pooling   | MEDIUM   | LOW    | P2         |
|      | in reporting service             |          |        |            |
+------+----------------------------------+----------+--------+------------+

Technical Debt Score: 34 points
Target: < 25 points
Trend: Decreasing (was 42 last month)

                 DEBT OVER TIME
    Points
    50 |    *
    40 |      *  *
    30 |            *  *
    20 |                  *
    10 |
     0 +--+--+--+--+--+--+--+--
       J  F  M  A  M  J  J  A
```

#### System Health Report

```
+==========================================================================+
|                     MONTHLY SYSTEM HEALTH REPORT                         |
|                          January 2026                                    |
+==========================================================================+

AVAILABILITY
------------
    Target: 99.9%    Actual: 99.97%    Status: EXCEEDS TARGET

    Week 1: 100.00%  [##########]
    Week 2:  99.95%  [#########.]
    Week 3:  99.98%  [##########]
    Week 4:  99.96%  [#########.]

PERFORMANCE
-----------
    Metric              Target      Actual      Status
    --------------------------------------------------------
    Avg Response Time   < 200ms     142ms       OK
    P95 Response Time   < 500ms     380ms       OK
    P99 Response Time   < 1000ms    720ms       OK
    Throughput          > 1000/s    1450/s      OK

INCIDENTS
---------
    Severity    Count   MTTR        Trend
    ----------------------------------------
    Critical    0       --          same
    High        1       32 min      improved
    Medium      3       2.1 hr      same
    Low         5       8 hr        same

ERROR BUDGET
------------
    Monthly Budget: 43.2 minutes (99.9% SLA)
    Used: 12.8 minutes (29.6%)
    Remaining: 30.4 minutes

    [========                              ] 29.6% used

RECOMMENDATIONS
---------------
1. Consider scaling up during peak hours (Mon 9-11 AM)
2. Investigate slow queries in reporting service
3. Plan migration from deprecated auth library

+==========================================================================+
```

#### Change Log / Release Notes

```
+==========================================================================+
|                         CHANGELOG                                        |
+==========================================================================+

## [1.3.0] - 2026-01-15

### Added
- User profile image upload feature
- Export orders to CSV functionality
- Rate limiting on public API endpoints

### Changed
- Improved search algorithm performance by 40%
- Updated payment gateway SDK to v3.2.0
- Migrated user sessions to Redis

### Fixed
- [BUG-042] Payment fails silently on expired cards
- [BUG-039] Order total calculation rounding error
- [BUG-041] Memory leak in websocket connections

### Security
- Patched XSS vulnerability in product descriptions
- Updated dependencies with known CVEs

### Deprecated
- Legacy /api/v1/auth/* endpoints (use /api/v2/auth/*)

---

## [1.2.0] - 2025-12-20

### Added
- Multi-currency support
- Order tracking notifications
- Admin bulk operations

### Changed
- Redesigned checkout flow
- Improved mobile responsiveness

### Fixed
- [BUG-035] Duplicate orders on double-click
- [BUG-036] Timezone issues in order history

+==========================================================================+
```

#### Roadmap Visualization

```
+==========================================================================+
|                          PRODUCT ROADMAP 2026                            |
+==========================================================================+

    Q1 2026                Q2 2026                Q3 2026                Q4 2026
    +-----------------+    +-----------------+    +-----------------+    +-----------------+
    |                 |    |                 |    |                 |    |                 |
    | [x] OAuth 2.0   |    | [ ] Mobile App  |    | [ ] AI Search   |    | [ ] Multi-      |
    |     Migration   |    |     (iOS)       |    |     Feature     |    |     Vendor      |
    |                 |    |                 |    |                 |    |     Support     |
    | [x] Performance |    | [ ] Mobile App  |    | [ ] Personali-  |    |                 |
    |     Optim.      |    |     (Android)   |    |     zation      |    | [ ] Analytics   |
    |                 |    |                 |    |                 |    |     Dashboard   |
    | [ ] New Payment |    | [ ] Wishlist    |    | [ ] Subscrip-   |    |                 |
    |     Providers   |    |     Feature     |    |     tions       |    | [ ] API v3      |
    |                 |    |                 |    |                 |    |                 |
    +-----------------+    +-----------------+    +-----------------+    +-----------------+

    Legend:
    [x] = Completed
    [~] = In Progress
    [ ] = Planned

    THEME FOCUS:
    Q1: Foundation & Security
    Q2: Mobile Expansion
    Q3: Intelligence & Personalization
    Q4: Platform & Scale

+==========================================================================+
```

---

## ASCII Diagram Reference

### Box Drawing Characters

```
Single Line:
+---------+
|         |
+---------+

Double Line:
+=========+
|         |
+=========+

Mixed:
+=========+
|         |
+---------+
|         |
+=========+
```

### Arrow Styles

```
Arrows:
    -->     Right arrow
    <--     Left arrow
    <-->    Bidirectional

    |
    v       Down arrow

    ^
    |       Up arrow

    \
     \      Diagonal
      v
```

### Common Patterns

```
Flow:
    [A] --> [B] --> [C]

Tree:
    Root
    +-- Child 1
    |   +-- Grandchild 1
    |   +-- Grandchild 2
    +-- Child 2

Table:
    +-------+-------+-------+
    | Col 1 | Col 2 | Col 3 |
    +-------+-------+-------+
    | Data  | Data  | Data  |
    +-------+-------+-------+

Status:
    [ ] Todo
    [~] In Progress
    [x] Done
    [!] Blocked

Progress Bar:
    [=====     ] 50%
    [==========] 100%
```

### Complex Shapes

```
Diamond (Decision):
        /\
       /  \
      / ?? \
      \    /
       \  /
        \/

Cylinder (Database):
      ______
     /      \
    |________|
    |        |
    |        |
    |________|

Cloud:
       ___
     _/   \_
    /       \
    \_     _/
      \___/

Actor:
       O
      /|\
      / \
```

---

## Conclusion

ASCII Driven Development provides a universal, lightweight, and version-control-friendly approach to documenting software systems. By using plain-text diagrams throughout the development lifecycle, teams can:

1. **Communicate more effectively** - Everyone can read ASCII
2. **Track changes precisely** - Git diffs work perfectly
3. **Stay tool-agnostic** - No vendor lock-in
4. **Document as code** - Diagrams live with the codebase

```
+------------------------------------------------------------------+
|                                                                  |
|   "The best documentation is the one that gets maintained."     |
|                                                                  |
|   ASCII diagrams are easy to create, easy to update, and        |
|   impossible to lose in a proprietary format.                    |
|                                                                  |
+------------------------------------------------------------------+
```

---

*Document created following ASCII Driven Development principles.*
