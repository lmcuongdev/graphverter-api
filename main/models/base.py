import json
from datetime import datetime

import attr

from main import db
from main.libs.log import ServiceLogger
from main.libs.misc import safe_load_json

logger = ServiceLogger(__name__)


class TimestampMixin:
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class MetaDataMixin:
    _meta_data_type = dict
    _meta_data = db.Column('meta_data', db.Text, nullable=True)

    @property
    def meta_data(self):
        raw_meta_data = safe_load_json(self._meta_data, default_factory=dict)

        return self._meta_data_type(**raw_meta_data)

    @meta_data.setter
    def meta_data(self, data):
        if data is None:
            self._meta_data = None
            return

        if not isinstance(data, dict):
            data = attr.asdict(data)

        self._meta_data = json.dumps(data)
