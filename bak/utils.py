import os
from datetime import datetime, timezone

from alibabacloud_dts20200101.client import Client as DtsClient
from alibabacloud_tea_openapi.models import Config

PERF_KEYS = {
    "mysql": {
        "MemCpuUsage": ["MySQL_MemCpuUsage"],
        "QPSTPS": ["MySQL_QPSTPS"],
        "Sessions": ["MySQL_Sessions"],
        "COMDML": ["MySQL_COMDML"],
        "RowDML": ["MySQL_RowDML"],
        "SpaceUsage": ["MySQL_DetailedSpaceUsage"],
        "ThreadStatus": ["MySQL_ThreadStatus"],
        "MBPS": ["MySQL_MBPS"],
        "DetailedSpaceUsage": ["MySQL_DetailedSpaceUsage"]
    },
    "pgsql": {
        "MemCpuUsage": ["MemoryUsage", "CpuUsage"],
        "QPSTPS": ["PolarDBQPSTPS"],
        "Sessions": ["PgSQL_Session"],
        "COMDML": ["PgSQL_COMDML"],
        "RowDML": ["PolarDBRowDML"],
        "SpaceUsage": ["PgSQL_SpaceUsage"],
        "ThreadStatus": [],
        "MBPS": [],
        "DetailedSpaceUsage": ["SQLServer_DetailedSpaceUsage"]
    },
    "sqlserver": {
        "MemCpuUsage": ["SQLServer_CPUUsage"],
        "QPSTPS": ["SQLServer_QPS", "SQLServer_IOPS"],
        "Sessions": ["SQLServer_Sessions"],
        "COMDML": [],
        "RowDML": [],
        "SpaceUsage": ["SQLServer_DetailedSpaceUsage"],
        "ThreadStatus": [],
        "MBPS": [],
        "DetailedSpaceUsage": ["PgSQL_SpaceUsage"]
    }

}


def transform_to_iso_8601(dt: datetime, timespec: str):
    return dt.astimezone(timezone.utc).isoformat(timespec=timespec).replace("+00:00", "Z")


def transform_to_datetime(s: str):
    try:
        dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        dt = datetime.strptime(s, "%Y-%m-%d %H:%M")
    return dt


def transform_perf_key(db_type: str, perf_keys: list[str]):
    perf_key_after_transform = []
    for key in perf_keys:
        if key in PERF_KEYS[db_type.lower()]:
            perf_key_after_transform.extend(PERF_KEYS[db_type.lower()][key])
        else:
            perf_key_after_transform.append(key)
    return perf_key_after_transform


def compress_json_array(json_array: list[dict]):
    if not json_array or len(json_array) == 0:
        return ""
    compress_str = ";".join(json_array[0].keys())
    for item in json_array:
        compress_str += "|" + ";".join([str(item[key] if key in item else "") for key in json_array[0].keys()])
    return compress_str


def get_dts_client(region_id: str):
    config = Config(
        access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
        security_token=os.getenv('ALIBABA_CLOUD_SECURITY_TOKEN'),
        region_id=region_id,
        protocol="https",
        connect_timeout=10 * 1000,
        read_timeout=300 * 1000
    )
    client = DtsClient(config)
    return client


