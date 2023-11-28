```
python -m venv venv
. venv/Scripts/activate
```

```
pip install fastApi[all]
```

## Levantar el servidor
```
uvicorn main:app --reload
```

The command `uvicorn main:app` refers to:

`main`: the file `main.py` (the Python "module").
`app`: the object created inside of `main.py` with the line `app = FastAPI()`.
`--reload`: make the server restart after code changes. Only use for development.

## API documentation
### Swagger
```
127.0.0.1/docs
```
### ReDoc
```
127.0.0.1/redoc
```
### OpenApi
```
127.0.0.1/openapi.json
```