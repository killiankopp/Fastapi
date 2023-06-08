from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def root(request: Request):
    my_header = request.headers.get('test')
    return {"message": my_header}