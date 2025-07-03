import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any, List

from alibabacloud_dts20200101 import models as dts_20200101_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from mcp.server.fastmcp import FastMCP

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from utils import (get_dts_client)

logger = logging.getLogger(__name__)

mcp = FastMCP("Echo")

db_list = '''{
    "dtstest": {
        "name": "dtstest",
        "all": false,
        "Table": {
            "dts1": {
                "name": "dts1_tgt_202505131603",
                "all": true
            }
        }
    }
}
'''

reserved = '''{
    "targetTableMode": "0",
    "dbListCaseChangeMode": "default",
    "isAnalyzer": false,
    "eventMove": false,
    "tableAnalyze": false,
    "whitelist.dms.online.ddl.enable": false,
    "sqlparser.dms.original.ddl": true,
    "whitelist.ghost.online.ddl.enable": false,
    "sqlparser.ghost.original.ddl": false,
    "privilegeMigration": false,
    "definer": false,
    "privilegeDbList": "[]",
    "maxRetryTime": 43200,
    "retry.blind.seconds": 600,
    "srcSSL": "0",
    "srcMySQLType": "HighAvailability",
    "destSSL": "0",
    "a2aFlag": "2.0",
    "autoStartModulesAfterConfig": "none"
}
'''


@mcp.tool()
async def configure_dts_job(
        region_id: str,
        job_type: str,
        dts_job_id: str,
        source_endpoint_region: str,
        source_endpoint_instance_type: str,
        source_endpoint_engine_name: str,
        source_endpoint_instance_id: str,
        source_endpoint_user_name: str,
        source_endpoint_password: str,
        destination_endpoint_region: str,
        destination_endpoint_instance_type: str,
        destination_endpoint_engine_name: str,
        destination_endpoint_instance_id: str,
        destination_endpoint_user_name: str,
        destination_endpoint_password: str
) -> Dict[str, Any]:
    """Configure a dts job.

    Args:
        region_id: Region ID.
        job_type: The type of job (synchronization job: SYNC, migration job: MIGRATION, data check job: CHECK).
        dts_job_id: The dts job id.
        source_endpoint_region: The source endpoint region ID.
        source_endpoint_instance_type: The source endpoint instance type (RDS, ECS, EXPRESS, CEN, DG)
        source_endpoint_engine_name: The source endpoint engine name (MySQL, PostgreSQL, SQLServer)
        source_endpoint_instance_id: The source endpoint instance ID (e.g., "rm-xxx").
        source_endpoint_user_name: The source endpoint user name.
        source_endpoint_password: The source endpoint password.
        destination_endpoint_region: The destination endpoint region ID.
        destination_endpoint_instance_type: The destination endpoint instance type (RDS, ECS, EXPRESS, CEN, DG)
        destination_endpoint_engine_name: The destination endpoint engine name (MySQL, PostgreSQL, SQLServer)
        destination_endpoint_instance_id: The destination endpoint instance ID (e.g., "rm-xxx").
        destination_endpoint_user_name: The destination endpoint user name.
        destination_endpoint_password: The destination endpoint password.

    Returns:
        Dict[str, Any]: Response containing the configured job details.
    """
    try:
        client = get_dts_client(region_id)

        request = dts_20200101_models.ConfigureDtsJobRequest(
            region_id=region_id,
            dts_job_name='bingyutest',
            source_endpoint_instance_type=source_endpoint_instance_type,
            source_endpoint_engine_name=source_endpoint_engine_name,
            source_endpoint_instance_id=source_endpoint_instance_id,
            source_endpoint_region=source_endpoint_region,
            source_endpoint_user_name=source_endpoint_user_name,
            source_endpoint_password=source_endpoint_password,
            destination_endpoint_instance_type=destination_endpoint_instance_type,
            destination_endpoint_instance_id=destination_endpoint_instance_id,
            destination_endpoint_engine_name=destination_endpoint_engine_name,
            destination_endpoint_region=destination_endpoint_region,
            destination_endpoint_user_name=destination_endpoint_user_name,
            destination_endpoint_password=destination_endpoint_password,
            structure_initialization=True,
            data_initialization=True,
            data_synchronization=True,
            job_type=job_type,
            db_list=db_list,
            reserve=reserved
        )

        if len(dts_job_id) > 0:
            request.dts_job_id = dts_job_id
            
        runtime = util_models.RuntimeOptions()
        response = client.configure_dts_job_with_options(request, runtime)
        return response.body.to_map()

    except Exception as e:
        logger.error(f"Error occurred while configure dts job: {str(e)}")
        raise e

@mcp.tool()
async def create_dts_instance(
        region_id: str,
        type: str,
        source_region: str,
        destination_region: str,
        source_endpoint_engine_name: str,
        destination_endpoint_engine_name: str
) -> Dict[str, Any]:
    """Create a dts instance.

    Args:
        region_id: Region ID.
        type: The type of job (synchronization job: SYNC, migration job: MIGRATION, data check job: CHECK)
        source_region: The source endpoint region ID.
        destination_region: The source endpoint instance type (RDS, ECS, EXPRESS, CEN, DG)
        source_endpoint_engine_name: The source endpoint engine name (MySQL, PostgreSQL, SQLServer)
        destination_endpoint_engine_name: The source endpoint instance ID (e.g., "rm-xxx").

    Returns:
        Dict[str, Any]: Response containing the created dts instance details.
    """
    try:
        client = get_dts_client(region_id)

        request = dts_20200101_models.CreateDtsInstanceRequest(
            region_id=region_id,
            type=type,
            source_region=source_region,
            destination_region=destination_region,
            source_endpoint_engine_name=source_endpoint_engine_name,
            destination_endpoint_engine_name=destination_endpoint_engine_name,
            pay_type='PostPaid',
            quantity=1,
            min_du=1,
            max_du=16,
            instance_class='micro'
        )

        runtime = util_models.RuntimeOptions()
        response = client.create_dts_instance_with_options(request, runtime)
        return response.body.to_map()

    except Exception as e:
        logger.error(f"Error occurred while create dts instance: {str(e)}")
        raise e

@mcp.tool()
async def start_dts_job(
        region_id: str,
        dts_job_id: str
) -> Dict[str, Any]:
    """Start a dts job.

    Args:
        region_id: Region ID.
        dts_job_id: the dts job id.

    Returns:
        Dict[str, Any]: Response containing the start result details.
    """
    try:
        client = get_dts_client(region_id)

        request = dts_20200101_models.StartDtsJobRequest(
            region_id=region_id,
            dts_job_id=dts_job_id
        )

        runtime = util_models.RuntimeOptions()
        response = client.start_dts_job_with_options(request, runtime)
        return response.body.to_map()

    except Exception as e:
        logger.error(f"Error occurred while start dts job: {str(e)}")
        raise e

@mcp.tool()
async def get_current_time() -> Dict[str, Any]:
    """Get the current time.

    Returns:
        Dict[str, Any]: The response containing the current time.
    """
    try:
        # Get the current time
        current_time = datetime.now()

        # Format the current time as a string
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # Return the response
        return {
            "current_time": formatted_time
        }
    except Exception as e:
        logger.error(f"Error occurred while getting the current time: {str(e)}")
        raise Exception(f"Failed to get the current time: {str(e)}")


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')