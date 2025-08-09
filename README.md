# URL Shortener

A **FastAPI**-based URL shortener with Docker support.  
It allows users to shorten URLs with custom keywords, track the number of clicks, and record the timestamp of each click.

## Features
- Shorten any URL
- Option to use a **custom keyword**
- Track **number of clicks** for each link
- Record **timestamps** of clicks
- Fully containerized using **Docker**

## Tech Stack
- **FastAPI** (Backend API)
- **SQLite/MySQL** (Configurable database)
- **SQLAlchemy** (ORM)
- **Docker** (Containerization)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/janakiramayya04/url_shortner.git
cd url_shortner
```
## 2. Install dependencies
```bash
pip install -r requirements.txt
```
## 3. Run using Docker
```bash
docker build -t url_shortener .
docker run -p 8000:8000 url_shortener
```
## 4. Access the API
```arduino
http://127.0.0.1:8000/docs
```
## API Endpoints
## Create a shortened URL
``` bash
POST /shorten
```
Body
``` json
{
  "url": "https://example.com",
  "custom_keyword": "mykeyword"
}
```
## Get click status
``` bash
GET /status/{keyword}
```
# Returns:




