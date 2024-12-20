# **Project: Domain Status Checker**

This project is designed to check the status of website domains, development on linux(ubuntu), using asynchronous techniques to perform the verification efficiently and quickly. The system is capable of determining whether a domain is "ON" (online) or "OFF" (offline), and it also collects information such as HTTP status, page content, and other connectivity parameters.

## **Features**

 - HTTP Status Check: Verifies the HTTP status code returned by the request, such as 200 OK, 404 Not Found, 503 Service Unavailable, and others.
 - Page Content: Checks if the website contains content (if the page is loading correctly).
 - Geolocation: Retrieves information about the server's country of origin.
 - Asynchronous Execution: Utilizes asynchronous functions to perform multiple domain checks concurrently without blocking the process.

## **Technologies Used**

 - Python: Programming language used for development.
 - Flask: Web framework to create the RESTful API.
 - SQLAlchemy: ORM for interacting with the database.
 - Playwright: Browser automation tool used for interacting with websites programmatically.
 - Asyncio: Library for asynchronous programming, used to perform multiple requests concurrently without blocking.

## **Installation**

1. **Clone the Repository**

 First, clone the repository:

 git clone https://github.com/your-username/repository-name.git

2. **Install Dependencies**

Install the project dependencies in a virtual environment:

```python

 cd repository-name 
 python3 -m venv .my_venv
 source .my_venv/bin/activate  

 pip install -r requirements.txt

```

3. **Database Setup**

    This project uses SQLAlchemy to interact with the database. Make sure to configure your database before running the application.

4. **Running the Application**
 
 To run the application, simply execute the main file:

```python

python run.py

```

The API will be available at http://127.0.0.1:5000/ by default.

## API Endpoints

1. **/domain_ansync (GET)**

 This endpoint performs an asynchronous check for multiple domains.

 Example Request:

```python
    
    curl http://127.0.0.1:5000/domain_ansync

```

 Response:

 {
    "message": "Domains scanned successfully"
 }


By: Ethercity
Create: Guilherme Ribeiro