# URL Shortener  [![Docker Pulls](https://img.shields.io/docker/pulls/janakiramayya/url-shortner-app)](https://hub.docker.com/r/janakiramayya/url-shortner-app)


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
- Click count
- Last clicked timestamp

## License
 This project is licensed under the MIT License.


<img width="1468" height="941" alt="image" src="https://github.com/user-attachments/assets/b41e50c5-5290-469c-8fac-9269cceb9273" />

<img width="1363" height="816" alt="image" src="https://github.com/user-attachments/assets/261c2f9b-105d-45c9-a5f3-b49923af5ec5" />

<img width="1225" height="643" alt="image" src="https://github.com/user-attachments/assets/34cffde2-3d27-46bb-b027-5491790fb7f6" />

<img width="1212" height="731" alt="image" src="https://github.com/user-attachments/assets/17349181-1d1f-490d-9eec-720469572a98" />

<img width="1208" height="987" alt="image" src="https://github.com/user-attachments/assets/38cd381f-d6c4-4113-a7e1-3f28c3910922" />




