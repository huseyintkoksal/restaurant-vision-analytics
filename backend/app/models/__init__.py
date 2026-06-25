"""SQLModel database models.

Important privacy note: there is **no** model for a person, face, identity, or
biometric template — by design. The schema stores only configuration objects
(cameras, zones) and **aggregate, anonymous** analytics (counts and pressures).
"""

from app.models.alert import Alert, AlertRead, AlertSeverity, AlertType
from app.models.analytics_snapshot import AnalyticsSnapshot, AnalyticsSnapshotRead
from app.models.camera import Camera, CameraCreate, CameraRead, CameraStatus
from app.models.privacy import PrivacyStatus, RetentionPolicy
from app.models.zone import ZoneCreate, ZoneRead, ZoneRecord

__all__ = [
    "Alert",
    "AlertRead",
    "AlertSeverity",
    "AlertType",
    "AnalyticsSnapshot",
    "AnalyticsSnapshotRead",
    "Camera",
    "CameraCreate",
    "CameraRead",
    "CameraStatus",
    "PrivacyStatus",
    "RetentionPolicy",
    "ZoneCreate",
    "ZoneRead",
    "ZoneRecord",
]
