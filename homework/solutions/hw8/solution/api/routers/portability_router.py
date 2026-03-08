from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from solution.services.data_portability_service import DataPortabilityService
from solution.api.dependencies import get_portability_service
from starlette.responses import FileResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
)

router = APIRouter(prefix="/portability", tags=["Portability"])
portability_service_dependency: DataPortabilityService = Depends(
    get_portability_service
)
import_file: UploadFile = File(...)


@router.get("/export", status_code=HTTP_200_OK)
def export_data(
    service: DataPortabilityService = portability_service_dependency,
) -> FileResponse:
    try:
        zip_path: str = service.export()
    except Exception as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))
    return FileResponse(zip_path, filename="all_data.zip")


@router.post("/import", status_code=HTTP_201_CREATED)
def import_data(
    file: UploadFile = import_file,
    service: DataPortabilityService = portability_service_dependency,
) -> dict[str, str]:

    if not file.filename.endswith(".zip"):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="File must be a .zip"
        )
    try:
        service.import_from_zip(file.file)
    except ValueError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(error))

    return {"message": "Data imported successfully"}
