from fastapi import APIRouter, FastAPI
import uvicorn

from article.routers.router import router as article_router
from comment.routers.router import router as comment_router


def get_app(*routers: APIRouter) -> FastAPI:
    app = FastAPI()

    for router in routers:
        app.include_router(router, prefix='/api')

    return app


app = get_app(article_router, comment_router)

if __name__ == '__main__':
    uvicorn.run(app)
