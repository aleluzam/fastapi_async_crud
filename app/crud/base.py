from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, false
from typing import TypeVar
from pydantic import BaseModel

CreateSchemaType = TypeVar("CreateSChemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ModelType = TypeVar("ModelType")


class CRUDBase():
    def __init__(self, model):
        self.model = model
    
    #### GET ####
    
    #obtener todos de una tabla
    async def get_all(self, db: AsyncSession):
        try:
            result = await db.execute(select(self.model).where(self.model.is_deleted == false()))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise
        
    # cualquiera por id
    async def get_by_id(self, id: int, db: AsyncSession):
        try:
            result = await db.execute(select(self.model).where(self.model.id == id, self.model.is_deleted == false()))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            await db.rollback()
            raise
        
    # obtener uno segun parametro
    async def get_one_by_paramater(self, parameter: str, value: str, db: AsyncSession):
        try:
            column = getattr(self.model, parameter)
    
            result = await db.execute(select(self.model).where(column == value, self.model.is_deleted == false()))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise
    
    #### POST & PUT ####
    
    
    # agregar
    async def create(self, db: AsyncSession, new_obj: CreateSchemaType) -> ModelType:
        try:
            obj_dict = new_obj.model_dump(exclude_unset=True)
            db_obj = self.model(**obj_dict)
            
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            
            return db_obj
        
        except SQLAlchemyError as e:
            await db.rollback()
            raise
        

    # actualizar
    async def update(self, db: AsyncSession, updt_obj: UpdateSchemaType, id: int) -> ModelType:
        try:
            obj_dict = updt_obj.model_dump(exclude_unset=True)
            
            result =  await db.execute(select(self.model).where(self.model.id == id))
            db_obj = result.scalar_one_or_none()
            if not db_obj:
                raise ValueError(f"Registro con id {id} no encontrado")
            
            for key, value in obj_dict.items():
                setattr(db_obj, key, value)

            await db.commit()
            await db.refresh(db_obj)
            return db_obj

        except ValueError:
            raise        
        
        except SQLAlchemyError:
            await db.rollback()
            raise
    
    async def soft_delete(self, db: AsyncSession, id: int) -> ModelType:
        try:
            result = await db.execute(select(self.model).where(self.model.id == id, self.model.is_deleted == false()))
            obj_to_delete = result.scalar_one_or_none()
            if not obj_to_delete:
                raise ValueError(f"Registro con id {id} no encontrado")
            
            obj_to_delete.is_deleted = True
            
            await db.commit()
            await db.refresh(obj_to_delete)
            
            return obj_to_delete
        
        except ValueError:
            raise
        
        except SQLAlchemyError:
            await db.rollback()
            raise