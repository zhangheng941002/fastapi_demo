#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2020/5/13 下午4:03
# @Author : Zh
# @Project : zh
# @File   : sql.py
# @Software: PyCharm

from app import settings

query_resource_by_sn = """

                        SELECT
                            t.FK_account_id,
                            t.FK_master_order_id,
                            t.master_resource_id,
                            t.start_date,
                            t.expire_date,
                            t.`status`,
                            t.resource_config,
                            t.contract_num,
                            t.is_to_business
                        FROM
                            {portal}.resource_manage t
                        WHERE
                            t.resource_config ->> '$.sdw_id' = (
                                SELECT
                                    id
                                FROM
                                    {resourcemanage}.sdw
                                WHERE
                                    sdw.sn = "{sn}"
                            )
                         
                        
                        
                        """.format(portal=settings.DB_PORTAL_NAME, resourcemanage=settings.DB_RESOURCE_MANAGE_NAME,
                                   sn="{sn}")

query_resource_by_order_no = """

                            SELECT
                                t.FK_account_id,
                                t.FK_master_order_id,
                                t.master_resource_id,
                                t.start_date,
                                t.expire_date,
                                t.`status`,
                                t.resource_config,
                                t.contract_num,
                                t.is_to_business
                            FROM
                                {portal}.resource_manage t
                            LEFT JOIN {portal}.master_order mo ON mo.master_order_id = t.FK_master_order_id and mo.master_order_no = "{order_no}"
                                
                            """.format(portal=settings.DB_PORTAL_NAME, order_no="{order_no}")

query_radius_attr = """

                    SELECT
                        cu.user_name,
                        cu.user_password,
                        cu.status user_status,
                        cua.attr_id,
                        cua.attr_value,
                        cua.status attr_status
                    FROM
                        {radius}.rd_cpe_user cu
                        LEFT JOIN {radius}.rd_cpe_user_attrs cua ON cua.user_id = cu.id 
                    WHERE
                        cu.user_name in {username}
                    """.format(radius=settings.DB_RADIUS_NAME, username="{username}")

# name map sql
name_data = {
    "query_resource_by_sn": query_resource_by_sn,
    "query_resource_by_order_no": query_resource_by_order_no,
    "query_radius_attr_by_sn": query_radius_attr,
}

# field map
data_format = {
    "query_resource_by_sn": {
        0: "account_id",
        1: "master_order_id",
        2: "master_resource_id",
        3: "start_date",
        4: "expire_date",
        5: "status",
        6: "resource_config",
        7: "contract_num",
        8: "is_to_business",
    },
    "query_resource_by_order_no": {
        0: "account_id",
        1: "master_order_id",
        2: "master_resource_id",
        3: "start_date",
        4: "expire_date",
        5: "status",
        6: "resource_config",
        7: "contract_num",
        8: "is_to_business",
    },
    "query_radius_attr_by_sn": {
        0: "user_name",
        1: "user_password",
        2: "user_status",
        3: "attr_id",
        4: "attr_value",
        5: "attr_status"
    },
}

sql_name_format = {
    "query_resource_by_sn": "通过sn查询资源信息",
    "query_resource_by_order_no": "通过订单编号查询资源信息",
    "query_radius_attr_by_sn": "通过sn查询radius属性",
}

sql_field_map = {
    "query_resource_by_sn": "sn",
    "query_resource_by_order_no": "order_no",
    "query_radius_attr_by_sn": "sn",
}


if __name__ == '__main__':
    from utils.db_utils import DBReader

    sql = query_resource_by_sn.format(sn="csn-4230000254")
    resp = DBReader().readList(sql, parameters="limit 2,3")
    print(resp)
    print(len(resp))