from fastapi import APIRouter

from backend.controllers.social_media import social_media_integrator_factory
from backend.models.models import TelegramLogin2FAModel, TelegramLogin2FARequestModel

router = APIRouter(
    prefix="/telegram",
)


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
