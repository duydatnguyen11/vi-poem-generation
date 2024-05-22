import uvicorn
from fastapi import FastAPI, HTTPException, Response
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from loguru import logger
from pipeline import generating_poem

# Creating FastAPI instance
app = FastAPI(root_path="/poem-generation-service")


# Custom route to expose the OpenAPI JSON at /poem-generation-service/openapi.json
@app.get("/poem-generation-service/openapi.json")
async def get_open_api_endpoint():
    return JSONResponse(
        get_openapi(title="Poem Generation API", version="1.0.0", routes=app.routes)
    )


# Endpoint to generate poem
@app.post("/generate-poem/")
async def generate_poem(prompt: str):
    try:
        logger.info("Generating poem...")
        poetry = generating_poem(prompt)
        # Log the generated poem
        logger.info("Generated Poetry: {}", poetry)

        return poetry
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002)
