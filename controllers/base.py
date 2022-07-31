from sqlalchemy import inspect, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from controllers.errors import (
    ObjectDoestExistControllerException,
)
from db import engine


class BaseController:
    model = None

    async def create(self, data):
        new_object = await self._create(data=data, model=self.model)
        return new_object

    async def get_one(
        self,
        filters: dict = None,
        join_relationships: list = None,
        raise_not_exists_exception=True,
    ):
        """
        :param raise_not_exists_exception: Allow raise exception on not exists
        :param join_relationships: Model fields for include to sql join tables
        :parameter filters: {model_field: value}

        filters: Allowed only equals filter operations
        """
        data = await self._get_one(
            model=self.model,
            filters=filters,
            join_relationships=join_relationships,
            raise_not_exists_exception=raise_not_exists_exception,
        )
        return data

    async def get_by_id(
        self, pk, join_relationships: list = None, raise_not_exists_exception=True
    ):
        data = await self._get_by_id(
            model=self.model,
            pk=pk,
            join_relationships=join_relationships,
            raise_not_exists_exception=raise_not_exists_exception,
        )
        return data

    async def get_many(
        self,
        filters: dict = None,
        limit=None,
        offset=None,
        join_relationships: list = None,
    ):
        """
        :param join_relationships: Model fields for include to sql join tables
        :param offset: Offset items
        :param limit: Limit items
        :parameter filters: {model_field: value}

        filters: Allowed only equals filter operations
        """
        data = await self._get_many(
            model=self.model,
            filters=filters,
            limit=limit,
            offset=offset,
            join_relationships=join_relationships,
        )
        return data

    async def count(
        self,
        filters: dict = None,
    ):
        """
        :parameter filters: {model_field: value}
        filters: Allowed only equals filter operations
        """
        data = await self._count(model=self.model, filters=filters)
        return data

    async def update(self, pk, data):
        await self._update(model=self.model, pk=pk, data=data)

    async def delete(self, pk):
        await self._delete(model=self.model, pk=pk)

    @classmethod
    def __get_id_filter(cls, model, pk):
        pk_key = inspect(model).primary_key[0].name
        return {pk_key: pk}

    async def _count(
        self,
        model,
        filters: dict = None,
    ):
        queryset = select(func.count()).select_from(model).filter_by(**filters)
        result = await self._async_session.execute(queryset)
        return result.scalar_one()

    async def _create(self, model, data):
        new_object = model(**data)
        self._async_session.add(new_object)
        await self._async_session.commit()
        await self._async_session.refresh(new_object)
        return new_object

    async def _update(self, model, pk, data):
        filters = self.__get_id_filter(model, pk)
        queryset = (
            update(model)
            .filter_by(**filters)
            .values(data)
            .execution_options(synchronize_session="fetch")
        )
        await self._async_session.execute(queryset)
        await self._async_session.commit()

    async def _delete(self, model, pk):
        filters = self.__get_id_filter(model, pk)
        queryset = delete(model).filter_by(**filters)
        await self._async_session.execute(queryset)
        await self._async_session.commit()

    async def _get_by_id(
        self,
        model,
        pk,
        join_relationships: list = None,
        raise_not_exists_exception=True,
    ):
        filters = self.__get_id_filter(model, pk)
        data = await self._get_one(
            model=model,
            filters=filters,
            join_relationships=join_relationships,
            raise_not_exists_exception=raise_not_exists_exception,
        )
        return data

    @classmethod
    def __get_base_select_query(
        cls,
        model,
        filters: dict = None,
        join_relationships: str = None,
    ):
        if not filters:
            filters = {}
        if not join_relationships:
            join_relationships = []
        if not isinstance(join_relationships, list):
            join_relationships = [join_relationships]
        queryset = select(model)
        for join_relationship in join_relationships:
            queryset = queryset.options(joinedload(join_relationship))
        queryset = queryset.filter_by(**filters)
        return queryset

    async def _get_one(
        self,
        model,
        filters: dict = None,
        join_relationships: list = None,
        raise_not_exists_exception=True,
    ):
        queryset = self.__get_base_select_query(
            model=model, filters=filters, join_relationships=join_relationships
        )
        result = await self._async_session.execute(queryset)
        data = result.scalars().first()
        if not data and raise_not_exists_exception:
            raise ObjectDoestExistControllerException(model=model, filters=filters)
        return data

    async def _get_many(
        self,
        model,
        filters: dict = None,
        limit=None,
        offset=None,
        join_relationships: str = None,
    ):
        queryset = self.__get_base_select_query(
            model=model, filters=filters, join_relationships=join_relationships
        )
        if limit is not None:
            queryset = queryset.limit(limit)
        if offset:
            queryset = queryset.offset(offset)
        result = await self._async_session.execute(queryset)
        return result.unique().scalars().all()

    def __int__(self):
        self._async_session = AsyncSession(engine)

    async def __aenter__(self, *args, **kwargs) -> "BaseController":
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self._async_session.close()
