from fastapi import APIRouter

from backend.controllers.predict_social_media import \
    predict_from_social_media_post
from backend.controllers.social_media import social_media_integrator_factory
from backend.models.models import (PredictionRequestURL, TelegramLogin2FAModel,
                                   TelegramLogin2FARequestModel)

router = APIRouter()


@router.get("/")
def ping():
    return {"message": "Hello World"}


@router.post("/telegram/send_login")
async def send_2fa_login_code(request: TelegramLogin2FARequestModel):
    integrator = social_media_integrator_factory.get_integrator("telegram")
    await integrator.get_2fa_code(request.phone_number)


@router.post("/telegram/login")
async def telegram_login(request: TelegramLogin2FAModel):
    integrator = social_media_integrator_factory.get_integrator("telegram")
    await integrator.sign_in(request.phone_number, request.code)


@router.post("/telegram/logout")
async def telegram_logout():
    integrator = social_media_integrator_factory.get_integrator("telegram")
    await integrator.sign_out()


@router.post("/predict/url")
async def predict_from_url(url: PredictionRequestURL):
    processed_url = str(url.url)
    result = await predict_from_social_media_post(processed_url)
    return {
        "url": processed_url,
        "result": result,
    }
