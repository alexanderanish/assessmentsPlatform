from fastapi import APIRouter, Body, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.users.models import UserDB
from app.users.users import current_active_user
from .models import ProgramModel, UpdateProgramModel


def get_program_router(app):

    router = APIRouter()

    @router.post(
        "/",
        response_description="Add new program",
    )
    async def create_program(
        request: Request,
        user: UserDB = Depends(current_active_user),
        program: ProgramModel = Body(...),
    ):
        program = jsonable_encoder(program)
        new_program = await request.app.db["programs"].insert_one(program)
        created_program = await request.app.db["programs"].find_one(
            {"_id": new_program.inserted_id}
        )

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_program)

    @router.get("/", response_description="List all programs")
    async def list_programs(
        request: Request,
        user: UserDB = Depends(current_active_user),
    ):
        programs = []
        for doc in await request.app.db["programs"].find().to_list(length=100):
            programs.append(doc)
        return programs

    @router.get("/{id}", response_description="Get a single program")
    async def show_program(
        id: str,
        request: Request,
        user: UserDB = Depends(current_active_user),
    ):
        if (program := await request.app.db["programs"].find_one({"_id": id})) is not None:
            return program

        raise HTTPException(status_code=404, detail=f"Program {id} not found")

    @router.put("/{id}", response_description="Update a program")
    async def update_program(
        id: str,
        request: Request,
        user: UserDB = Depends(current_active_user),
        program: UpdateProgramModel = Body(...),
    ):
        program = {k: v for k, v in program.dict().items() if v is not None}

        if len(program) >= 1:
            update_result = await request.app.db["programs"].update_one(
                {"_id": id}, {"$set": program}
            )

            if update_result.modified_count == 1:
                if (
                    updated_program := await request.app.db["programs"].find_one({"_id": id})
                ) is not None:
                    return updated_program

        if (
            existing_program := await request.app.db["programs"].find_one({"_id": id})
        ) is not None:
            return existing_program

        raise HTTPException(status_code=404, detail=f"Program {id} not found")

    @router.delete("/{id}", response_description="Delete Program")
    async def delete_program(
        id: str,
        request: Request,
        user: UserDB = Depends(current_active_user),
    ):
        delete_result = await request.app.db["programs"].delete_one({"_id": id})

        if delete_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(status_code=404, detail=f"Program {id} not found")

    return router