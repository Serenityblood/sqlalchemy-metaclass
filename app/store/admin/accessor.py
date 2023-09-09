import typing
from hashlib import sha256

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor
from app.web.app import Application

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        # TODO: создать админа по данным в config.yml здесь
        self.app = app
        try:
            await self.create_admin(
                email=self.app.config.admin.email,
                password=sha256(self.app.config.admin.password.encode()).hexdigest()
            )
        except IntegrityError:
            return None

    async def get_by_email(self, email: str) -> Admin:
        async with self.app.database.session.begin() as session:
            result = await session.execute(select(AdminModel).where(AdminModel.email == email))
            try:
                admin = result.scalar_one()
                return Admin(admin.id, admin.email, admin.password)
            except NoResultFound:
                return None

    async def create_admin(self, email: str, password: str) -> Admin:
        admin = AdminModel(email=email, password=password)
        async with self.app.database.session.begin() as session:
            session.add(admin)
            await session.commit()
        return admin
