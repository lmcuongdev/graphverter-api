from typing import Optional

from main import db
from main.enums import VersionStatus
from main.libs.log import ServiceLogger
from main.models.version import VersionModel

logger = ServiceLogger(__name__)


def create_version(
    project_id: int,
    version_data: dict,
    status: str = VersionStatus.ACTIVE,
    is_dirty: bool = False,
    **__,
) -> VersionModel:
    version = VersionModel(
        project_id=project_id,
        meta_data=version_data,
        status=status,
        is_dirty=is_dirty,
    )
    db.session.add(version)
    return version


def update_latest_version(
    project_id: int,
    **kwargs,
):
    version = get_latest_version(project_id)
    if not version:
        return

    update_version(version, **kwargs)


def get_latest_version(
    project_id: int,
    status: str = VersionStatus.ACTIVE,
) -> VersionModel:
    # TODO: Load from cache option
    return (
        VersionModel.query.filter_by(
            project_id=project_id,
            status=status,
        )
        .order_by(VersionModel.id.desc())
        .first()
    )


def update_version(
    version: VersionModel,
    version_data: Optional[dict] = None,
    status: Optional[str] = None,
    is_dirty: Optional[bool] = None,
    **kwargs,
):
    logger.info(
        message=f'Updating version #{version.id} data.',
        data=locals(),
    )

    if version_data is not None:
        version.meta_data = version_data
    if status is not None:
        version.status = status
    if is_dirty is not None:
        version.is_dirty = is_dirty

    db.session.commit()
