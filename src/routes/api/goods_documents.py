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

    if limit > 100: # Ставим лимит на максимальное количество выгрузки записей, чтобы не убить БД и сервер
        raise HTTPException(
            status_code=400,
            detail="лимит должен быть от 1 до 100"
        ) # Если число больше 100 - отдаём ошибку

    goods_documents = [] # Тут будут собраны все записи в конечном результате (на этапе сборки и выдачи пользователю)

    results = (await db.execute(( # Выполняем запрос
        select(
            Documents.id.label("document_id"), # Получаем ИД докумена
            func.json_build_object(
                'type_id', Documents.type_id,
                'name', Documents.name,
                'date', Documents.data,
                'person_id', Documents.person_id
            ).label("document_info"), # Из таблицы документов формируем JSON данных, в таблице Documents должны быть все эти поля
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
            ).label("items") # Из таблицы товаров формирует JSON данных, в таблице Goods должны быть все эти поля
        )
        .join(GoodsDocuments, GoodsDocuments.document_id == Documents.id) # Присоединяем таблицу документов
        .join(Goods, Goods.id == GoodsDocuments.item_id) # Присоединяем таблицу товаров
        .group_by(Documents.id) # Группируем goods_documents по document_id (чтобы сформировать общее по каждому документу, а не раздельно записи с одинаковыми ИД)
        .limit(limit) # Ставим лимит запроса записей (условно 25 шт нам нужно)
        .offset(offset) # Ставим оффсет (пропуск) записей
    ))).all() # говорим что из результата нам нужна не 1 строчка, а всё что выдала база на запрос

    for result in results:
        # Из полученных данных собираем каждую запись в нужном нам виде
        goods_documents.append({
            "id": result[0],
            "type_id": result[1]['type_id'],
            "person_id": result[1]['person_id'],
            "name": result[1]['name'],
            "date": result[1]['date'],
            "items": result[2]
        })

    # Пихаем всё в модель, отдаём пользователю
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
        )).scalar() # Получаем количество уникальных document_id (т.е. сколько документов у нас всего)
    )


# Вопросы? это все очень сложно, работа такая я бы так не написала вот в чем проблема Т_Т
# шанс на то, что я напишу так - практически нулевой, всё с ГПТ скатано подчистую
# тут просто надо работать долго с алхимией, а я мало с ней работал, в основном на монге сижу
# можешь сказать просто что я помог, идк нет, начнут придираться тогда если бы попроще все это выводить можно было, а  не так

"""

можно и попроще, в несколько запросов, но шанс того, что запрос будет грузиться овердохуя секунд - огромный
ибо в 3 запроса это решается так:

1. выгружаем все goods_documents (с группировкой document_id, иначе мы вообще не знаем тогда сколько в базе строк, которые необходимы под вывод)
типа, записи явно будут повторяться, надо как-то это проверять, а ебашить запросы while True пока не встретим новый ИД и не наберём 25 шт уникальных - бредово

2. по каждому документу мы выгружаем его данные, форматируем результат (этап сброки данных №1) - это ещё 25 запросов

3. в зависимости от того, как ты соберёшь item_id у всех документов - тоже разное кол-во запросов 

если это будет [item_id1, item_id2, item_id3...] - можно уложиться в 1 запрос для каждой записи
если же это всё оставить kak
document_id=12, item_id = 1,
document_id=12, item_id = 2,
document_id=12, item_id = 3,
document_id=12, item_id = 4,
то придётся делать N запросов к базе под каждый товар, что ещё больше увеличит время получения данных

Технически, то что написано выше - вообще САМЫЙ быстрый вариант выгрузки, быстрее только если оптимизировать базу
 что если временные таблицы под товары делать и выгружать их
 
звучит  на самом деле печально, я тебе больше скажу, у тебя пробоина в схеме базы
как бы то оно звучит прикольно в данный момент, ибо связь М-К-М, но можно оптимизировать это добро

если убрать поле item_id: int
и добавить items: int[] с foreign_key, он так тоже умеет
это сразу уменьшит поиск по базе и будет хранить все ID товаров у тебя

в таком случае можно потом ввести запрос
SELECT * FROM goods WHERE id IN (1, 2, 3...)

и он выведет информацию сразу по всем товарам, которые указаны в документе
ну так если это облегчит задачу то давай так и сделаем как айди туда поступать должны, через триггер?
идейно вообще когда не используешь crud_router, ты просто в поле добавляешь\удаляешь число, так доступно

"""