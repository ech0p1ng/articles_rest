from fastapi import APIRouter, Depends
from article.schemas.schema import ArticleSchema, ArticleSimpleSchema
from article.services.service import ArticleService
from dependencies.services import article_service
from article.models.model import ArticleModel

router = APIRouter(prefix='/articles', tags=['Статьи'])


@router.post(
    path='/',
    summary='Создание статьи',
    description='Создание статьи',
    response_model=ArticleSchema
)
async def create_article(
    schema: ArticleSimpleSchema,
    service: ArticleService = Depends(article_service)
):
    return await service.create(ArticleModel.from_schema(schema))


@router.get(
    path='/cached/{article_id}',
    summary='Получение кешированной статьи по ее ID',
    description='Получение кешированной статьи по ее ID',
    response_model=ArticleSchema
)
async def get_cached_article(
    article_id: int,
    service: ArticleService = Depends(article_service)
):
    return await service.get_cached(article_id)


@router.get(
    path='/trending',
    summary='Получение случайной статьи',
    description='Получение случайной статьи',
    response_model=ArticleSchema
)
async def get_article_tranding(
    service: ArticleService = Depends(article_service)
):
    return await service.get_tranding()


@router.get(
    path='/{article_id}',
    summary='Получение статьи по ее ID',
    description='Получение статьи по ее ID',
    response_model=ArticleSchema
)
async def get_article(
    article_id: int,
    service: ArticleService = Depends(article_service)
):
    return await service.get({"id": article_id})


@router.get(
    path='/',
    summary='Получение всех статей',
    description='Получение всех статей',
    response_model=list[ArticleSchema]
)
async def get_all_articles(
    service: ArticleService = Depends(article_service)
):
    return await service.get_all()
