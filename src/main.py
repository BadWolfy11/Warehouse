from routes import router
from core.config import settings
from core.setup import create_application
from fastapi.staticfiles import StaticFiles

import uvicorn

application = create_application(router=router, settings=settings)

application.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(application, host=settings.APP_HOST, port=settings.APP_PORT, log_level=settings.APP_LOG_LEVEL)