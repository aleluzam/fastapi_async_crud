from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import select, false
from typing import TypeVar
from pydantic import BaseModel
from fastapi import HTTPException, status

CreateSchemaType = TypeVar("CreateSChemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ModelType = TypeVar("ModelType")


class CRUDBase():
    def __init__(self, model):
        self.model = model
    
    #### GET ####
    
    #obtener todos de una tabla
    async def get_all(self, db: AsyncSession, include_deleted: bool = False):
        try:
            query = select(self.model)
            if not include_deleted:
                query = select(self.model).where(self.model.is_deleted == False)
            result = await db.execute(query)
            
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
    
    
    async def create(self, db: AsyncSession, new_obj: CreateSchemaType) -> ModelType:
        try:
            obj_dict = new_obj.model_dump(exclude_unset=True)
            
            if 'password' in obj_dict:
                obj_dict['password_hashed'] = obj_dict.pop('password')
            
            db_obj = self.model(**obj_dict)
            
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            
            return db_obj
        
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un registro con esos datos"
            )
        
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error de base de datos: {str(e)}"
            )

    # actualizar
    async def update(self, db: AsyncSession, updt_obj: UpdateSchemaType, id: int) -> ModelType:
        try:
            obj_dict = updt_obj.model_dump(exclude_unset=True)
            
            result =  await db.execute(select(self.model).where(self.model.id == id, self.model.is_deleted == false()))
            db_obj = result.scalar_one_or_none()
            if not db_obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"error": f"Registro de id {id} no encontrado"}
                )
            
            unchanged_fields = []
            changed_fields = []
            
            for key, new_value in obj_dict.items():
                actual_value = getattr(db_obj, key)
                
                if actual_value != new_value:
                    changed_fields.append(key)
                    setattr(db_obj, key, new_value)
                else:
                    unchanged_fields.append(key)
            
            if not changed_fields:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail={"error": f"Los campos {unchanged_fields} son identicos a los valores actuales"}
                )
                
            await db.commit()
            await db.refresh(db_obj)
            return db_obj

        except HTTPException:
            raise        
        
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de base de datos: {str(e)}"
            )    
            
    async def soft_delete(self, db: AsyncSession, id: int):
        try:
            result = await db.execute(select(self.model).where(self.model.id == id, self.model.is_deleted == false()))
            obj_to_delete = result.scalar_one_or_none()
            if not obj_to_delete:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Registro de id {id} no encontrado"
                )
            obj_to_delete.soft_delete()
            await db.commit()
            return {"message": "Elimination success"}
        except HTTPException:
            raise 
               
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de base de datos: {str(e)}"
            )    
