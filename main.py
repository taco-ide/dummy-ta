from fastapi import FastAPI
import os

app = FastAPI()

@app.get('/api/hello')
async def hello():
    return {"message": "Hello, World!"}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host='0.0.0.0', port=port)
