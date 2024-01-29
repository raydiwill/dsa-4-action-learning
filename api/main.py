from fastpi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8050)
