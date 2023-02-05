from fastapi import FastAPI

app = FastAPI()


@app.get("/sub/")
def read_sub():
    return {"message": "This is Sub app"}
