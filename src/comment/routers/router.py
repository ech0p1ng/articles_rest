from fastapi import APIRouter, Depends
from comment.schemas.schema import CommentSchema, CommentSimpleSchema
from comment.services.service import CommentService
from dependencies.services import comment_service
from comment.models.model import CommentModel

router = APIRouter(prefix='/comments', tags=['Коментарии'])


@router.get(
    path='/tranding',
    summary='Получение случайного коментария',
    description='Получение случайного коментария',
    response_model=CommentSchema
)
async def get_comment_tranding(
    service: CommentService = Depends(comment_service)
):
    return await service.get_trending()


@router.get(
    path='/{comment_id}',
    summary='Получение коментария по ее ID',
    description='Получение коментария по ее ID',
    response_model=CommentSchema
)
async def get_comment(
    comment_id: int,
    service: CommentService = Depends(comment_service)
):
    return await service.get({"id": comment_id})


@router.get(
    path='/',
    summary='Получение всех коментариев',
    description='Получение всех коментариев',
    response_model=list[CommentSchema]
)
async def get_all_comments(
    service: CommentService = Depends(comment_service)
):
    return await service.get_all()


@router.post(
    path='/add',
    summary='Создание коментария',
    description='Создание коментария',
    response_model=CommentSchema
)
async def create_comment(
    schema: CommentSimpleSchema,
    service: CommentService = Depends(comment_service)
):
    return await service.create(CommentModel.from_schema(schema))
