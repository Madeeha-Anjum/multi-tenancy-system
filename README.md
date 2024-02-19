# Multi Tenant System

## Installation

1. Clone the repository:

2. Create a virtual environment: (Optional but recommended)

    ```bash
    python3 -m venv .venv
    source .venv/Scripts/activate
    ```

3. Install dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the FastAPI application:

    ```bash
    uvicorn main:app --reload
    ```

2. Access the interactive API documentation:
   - Open your browser and go to [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.
   - Alternatively, access [http://localhost:8000/redoc](http://localhost:8000/redoc) for ReDoc.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
