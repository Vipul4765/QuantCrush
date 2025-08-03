# 🚀 QuantCrush: AI-Powered Candlestick Pattern Intelligence Platform

QuantCrush is a blazing-fast backend system designed for real-time candlestick pattern detection, intelligent pattern filtering, and per-symbol stock data analysis using advanced pattern recognition logic, all built using **FastAPI**, **PostgreSQL**, and **TA-Lib**.

> 🧠 Designed for financial analysts, traders, and quantitative researchers who demand performance, reliability, and precision.

---

## 🔥 Key Features

* 📊 Automatically detects 12+ well-known candlestick patterns
* 📦 Stores data in both **per-symbol tables** and a **centralized common table**
* ⚡ High-speed APIs for latest patterns and historical search
* 🔐 API key-based security for all endpoints
* 🧱 Smart database indexing for rapid querying
* 🔄 Daily automatic processing of NSE bhavcopy data
* 🛠️ Developer-friendly structure with clean separation of concerns

```

---

## 🏦 Database Design

### 1. `common_stock_data`

This table holds all daily stock data with recognized patterns.

| Column            | Type    | Description                   |
| ----------------- | ------- | ----------------------------- |
| symbol            | string  | Stock ticker (e.g., RELIANCE) |
| date              | date    | Trading date                  |
| open, high...     | float   | OHLCV data                    |
| pattern\_value    | integer | Encoded pattern ID (internal) |
| matched\_patterns | string  | Names of matched patterns     |

✔️ Indexed for lightning-fast filtering by `symbol`, `date`, `pattern_value`, etc.

### 2. `stock_<symbol>`

Each stock has its own table (e.g., `stock_infy`) for fast access, pagination, and historical analysis.

---

## 🤩 API Endpoints (All Secured via `X-API-KEY` Header)

### 📌 `/patterns/latest`

Get the latest patterns from all stocks, sorted by date.

**Example:**

```http
GET /patterns/latest?page=1&limit=20
```

---

### 🔍 `/patterns/search`

Search patterns by any combination of:

* Date range (`start_date`, `end_date`)
* Stock symbol
* Pattern type (internal encoding)

**Example:**

```http
GET /patterns/search?symbol=TCS&start_date=2025-07-15&end_date=2025-08-01
```

---

### 🧠 `/pattern-rank`

Get the full list of supported patterns for UI or filtering logic.

---

### 📜 `/stock/{symbol}`

Fetch pattern data for any specific stock (from its dedicated table).

**Example:**

```http
GET /stock/INFY?start_date=2025-07-01
```

---

## ⚙️ How It Works (Under the Hood)

1. Automatically downloads daily **NSE bhavcopy CSVs**
2. Cleans, transforms, and filters **EQ series only**
3. Applies candlestick pattern recognition using **TA-Lib**
4. Stores processed data in:

   * A **common global table** for pattern search
   * A **per-symbol table** for historical exploration
5. Indexes are applied for efficient filtering and search
6. All APIs serve data based on strict API key authentication

---

## 🧪 Supported Candlestick Patterns

* Hammer
* Inverted Hammer
* Doji (all types)
* Piercing Line
* Hanging Man
* Shooting Star
* Marubozu
* Spinning Tops
* … and more!

---

## 🔐 API Security

Every route is protected using a custom header:

```
Header:
X-API-KEY: your-secret-key
```

---

## 💼 Real-World Use Cases

* “Show me all stocks with **Hammer** or **Doji** in the last 5 days.”
* “Give me all pattern matches for **INFY** since July.”
* “Paginate the latest 100 pattern records for all NIFTY50 stocks.”
* “Rank stocks by strongest patterns today.”

---

## 📌 Tech Stack

| Layer         | Tech                      |
| ------------- | ------------------------- |
| Backend       | FastAPI                   |
| Pattern Logic | TA-Lib                    |
| Database      | PostgreSQL + SQLAlchemy   |
| Security      | Environment-based API key |
| Deployment    | Docker-ready (optional)   |

---

## 👨‍💼 Author

**Vipul Dhankar**
Python Backend Developer | Quant Systems Designer
[GitHub: @Vipul4765](https://github.com/Vipul4765)

---

## 📄 License

This project is licensed under **Private & Protected Build**
All rights reserved ©️ 2025
❌ **Do not copy, distribute, or reuse without permission**

---

## 🤝 Let’s Connect

Interested in AI-powered trading tools, backtesting, or high-speed market data systems?
Let’s collaborate!

📧 [vipuldhankar17170277@gmail.com](mailto:vipuldhankar17170277@gmail.com)
🌐 [LinkedIn](https://www.linkedin.com/in/vipul-kumar-5861221b9/)

---
