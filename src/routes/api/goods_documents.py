from fastapi import Depends, HTTPException
from fastcrud import crud_router
from sqlalchemy import select, func
from sqlalchemy import func
from src.core.models import GoodsDocuments, Goods, Documents

from core.database import get_async_session
from core.models import GoodsDocuments
from models.schemas.goods_documents import GoodsDocumentsCreate, GoodsDocumentsUpdate, GoodsDump


router = crud_router(
    session=get_async_session,
    model=GoodsDocuments,
    create_schema=GoodsDocumentsCreate,
    update_schema=GoodsDocumentsUpdate,
    path="/goods_documents",
    tags=["GoodsDocuments"],
)

@router.get(
    path='/goods_documents/dump',
    response_model=GoodsDump,
    # summary='Дамп множества записей',
    # response_description='Информация выгружена',

    tags=["GoodsDocuments"],
)
async def dump_goods(
    limit: int = 100,
    offset: int = 0,
    db = Depends(get_async_session)
) -> GoodsDump | HTTPException:
    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicGVyc29uX2lkIjoxLCJyb2xlX2lkIjoxLCJleHAiOjE3MzEyNjc5MTJ9.mXtzTA-c2KgZ4fshsN8lranOFBv0-Mdo3SuxDXGYXNM

    if limit > 100:
        raise HTTPException(
            status_code=400,
            detail="лимит должен быть от 1 до 100"
        )

    goods_documents = []

    results = await db.execute(
        select(
            Documents.id.label("document_id"),
            func.json_build_object(
                'type_id', Documents.type_id,
                'name', Documents.name,
                'date', Documents.data,
                'person_id', Documents.person_id
            ).label("document_info"),
            func.json_agg(
                func.json_build_object(
                    'id', Goods.id,
                    'barcode', Goods.barcode,
                    'name', Goods.name,
                    'description', Goods.description,
                    'category_id', Goods.category_id,
                    'attachments', Goods.attachments,
                    'quantity', GoodsDocuments.quantity
                )
            ).label("items")
        )
        .select_from(Documents)
        .outerjoin(GoodsDocuments, GoodsDocuments.document_id == Documents.id)
        .outerjoin(Goods, Goods.id == GoodsDocuments.item_id)
        .group_by(Documents.id)
        .limit(limit)
        .offset(offset)
    )

    for result in results:

        goods_documents.append({
            "id": result[0],
            "type_id": result[1]['type_id'],
            "person_id": result[1]['person_id'],
            "name": result[1]['name'],
            "date": result[1]['date'],
            "items": result[2]
        })


    return GoodsDump(
        documents=goods_documents,
        total=(await db.execute(
            select(
                func.count(
                    func.distinct(
                        GoodsDocuments.document_id
                    )
                ).label("documents_count")
            )
        )).scalar()
    )

