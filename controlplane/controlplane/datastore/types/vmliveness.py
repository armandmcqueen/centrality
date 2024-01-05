import datetime
from pydantic import BaseModel
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from controlplane.datastore.types.base import DatastoreBaseORM


class VmInfoOrm(DatastoreBaseORM):
    __tablename__ = "vm_info"
    vm_id: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    last_heartbeat_ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    registration_ts: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    num_cpus: Mapped[int] = mapped_column(nullable=False)
    cpu_description: Mapped[str] = mapped_column(nullable=False)
    host_memory_mb: Mapped[int] = mapped_column(BigInteger, nullable=False)
    num_gpus: Mapped[int] = mapped_column(nullable=False)
    gpu_type: Mapped[str] = mapped_column(nullable=True)
    gpu_memory_mb: Mapped[int] = mapped_column(BigInteger, nullable=True)
    nvidia_driver_version: Mapped[str] = mapped_column(nullable=True)
    hostname: Mapped[str] = mapped_column(nullable=False)


class VmInfo(BaseModel):
    """
    Information about a VM's current state
    """

    # IMPORTANT: If you change this, you must also change the VmRegistration class below
    vm_id: str
    last_heartbeat_ts: datetime.datetime
    registration_ts: datetime.datetime
    num_cpus: int
    cpu_description: str
    host_memory_mb: int
    num_gpus: int
    gpu_type: Optional[str]
    gpu_memory_mb: Optional[int]
    nvidia_driver_version: Optional[str]
    hostname: str

    @classmethod
    def from_orm(cls, orm: VmInfoOrm) -> "VmInfo":
        return cls(
            vm_id=orm.vm_id,
            last_heartbeat_ts=orm.last_heartbeat_ts,
            registration_ts=orm.registration_ts,
            num_cpus=orm.num_cpus,
            cpu_description=orm.cpu_description,
            host_memory_mb=orm.host_memory_mb,
            num_gpus=orm.num_gpus,
            gpu_type=orm.gpu_type,
            gpu_memory_mb=orm.gpu_memory_mb,
            nvidia_driver_version=orm.nvidia_driver_version,
            hostname=orm.hostname,
        )

    def to_orm(self) -> VmInfoOrm:
        return VmInfoOrm(
            vm_id=self.vm_id,
            last_heartbeat_ts=self.last_heartbeat_ts,
            registration_ts=self.registration_ts,
            num_cpus=self.num_cpus,
            cpu_description=self.cpu_description,
            host_memory_mb=self.host_memory,
            num_gpus=self.num_gpus,
            gpu_type=self.gpu_type,
            gpu_memory_mb=self.gpu_memory,
            nvidia_driver_version=self.nvidia_driver_version,
            hostname=self.hostname,
        )


class VmRegistrationInfo(BaseModel):
    """
    Information about a VM to register with the control plane.

    Same as VM heartbeat, but without a few fields that are either set via URL params or
    automatically set server-side.
    """

    num_cpus: int
    cpu_description: str
    host_memory_mb: int
    num_gpus: int
    gpu_type: Optional[str]
    gpu_memory_mb: Optional[int]
    nvidia_driver_version: Optional[str]
    hostname: str

    def to_vm_info_orm(self, vm_id: str) -> VmInfoOrm:
        return VmInfoOrm(
            vm_id=vm_id,
            last_heartbeat_ts=datetime.datetime.now(datetime.timezone.utc),
            registration_ts=datetime.datetime.now(datetime.timezone.utc),
            num_cpus=self.num_cpus,
            cpu_description=self.cpu_description,
            host_memory_mb=self.host_memory_mb,
            num_gpus=self.num_gpus,
            gpu_type=self.gpu_type,
            gpu_memory_mb=self.gpu_memory_mb,
            nvidia_driver_version=self.nvidia_driver_version,
            hostname=self.hostname,
        )
