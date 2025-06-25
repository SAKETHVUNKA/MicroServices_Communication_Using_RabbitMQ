# 🧩 Microservices Architecture with RabbitMQ

This project is a full-stack microservices-based inventory and order management system built using **Python Flask**, **RabbitMQ**, **MySQL**, and **Docker**. It demonstrates asynchronous communication using message queues, decoupled services, and scalable design.

## 🗂️ Project Structure

```
microservices-with-rabbitmq/
│
├── docker-compose.yml
├── database_service/
│   ├── Dockerfile
│   └── init.sql
├── frontend/
│   ├── static
│   ├── templates
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── producer/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── producer.py
├── consumer_one/       # Container Health Checker
│   ├── Dockerfile
│   ├── requirements.txt
│   └── health_check.py
├── consumer_two/       # Item Creator
│   ├── Dockerfile
│   ├── requirements.txt
│   └── item_creation.py
├── consumer_three/     # Stock Management
│   ├── Dockerfile
│   ├── requirements.txt
│   └── stock_management.py
├── consumer_four/      # Order Processor
│   ├── Dockerfile
│   ├── requirements.txt
│   └── order_processing.py
```

## ⚙️ Services

| Service         | Description                                 | Port        |
|----------------|---------------------------------------------|-------------|
| `frontend`      | User-facing Flask app                       | `8001`      |
| `producer`      | Main API router to queue messages           | `5555`      |
| `rabbitmq`      | RabbitMQ + Management UI                    | `5672` (msg), `15673` (UI) |
| `database`      | MySQL DB with inventory schema              | `3307`      |
| `consumer_one`  | Checks Docker container health              | -           |
| `consumer_two`  | Handles item creation requests              | -           |
| `consumer_three`| Manages stock (fetch/update)                | -           |
| `consumer_four` | Processes orders and tracks them            | -           |

## 🧪 Features

- 🔁 Asynchronous message passing using RabbitMQ
- 🛒 Inventory and Order tracking
- ✅ Container Health checks
- 📦 Modular microservice design
- 🐬 MySQL-based persistent storage
- 🐳 Fully Dockerized

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/SAKETHVUNKA/microservices-with-rabbitmq.git
cd microservices-with-rabbitmq
```

### 2. Start Docker Services

Ensure Docker is installed. Then run:

```bash
docker-compose up --build
```

RabbitMQ UI: http://localhost:15673  
Frontend: http://localhost:8001

> 📌 Login for RabbitMQ UI (if prompted):  
> Username: `guest` | Password: `guest`

## 🌐 Frontend Routes

| Route                 | Description                            |
|-----------------------|----------------------------------------|
| `/`                   | Homepage                               |
| `/healthcheck`        | Check status of any container          |
| `/additem`            | Add new product to inventory           |
| `/edititem/<id>`      | Update existing product                |
| `/sellitem`           | Add item to cart                       |
| `/addorder`           | Finalize order                         |
| `/stockmanagement`    | View all inventory data                |
| `/ordertracking`      | View placed orders                     |
| `/changestatus/<id>`  | Update order status                    |
| `/display_items/<id>` | View items in a specific order         |

## 🛢️ Database Schema

Includes 4 core tables:

- `Products`
- `Suppliers`
- `Orders`
- `Order_Items`

SQL schema is defined in `database_service/init.sql`.

## 📬 Message Flow (Simplified)

```
[Frontend] → HTTP → [Producer API]
         ↓                        ↓
   [RabbitMQ] ← (enqueue) ← Queue ← [Consumers]
         ↓
   [Producer API] ← (response) ← [Consumers]
         ↓
   [Frontend] ← polling ← /response
```

## 📝 Notes

- Uses **correlation IDs** to pair requests/responses in async calls.
- Uses **Docker socket API** for container health check.
- RabbitMQ is used for all inter-service communication.
- Code is modular and designed for easy scaling.

## 📦 Requirements

- Docker & Docker Compose
- (Optional for local testing) Python 3.8+, MySQL Server, RabbitMQ

## ✍️ Author

 - [Naga Saketh V](https://github.com/SAKETHVUNKA)
 - [Adnan Zaki](https://github.com/zaki-1337)

---