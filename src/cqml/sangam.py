# Sangam Configuration for QUILT
from .db2quilt import Project, save_table

ORG="nauto"
BUCKET="biz-databricks-root-prod-us"
PROJECT="sangam"

ORG="nauto"
BUCKET="biz-databricks-root-prod-us"
PROJECT="sangam"
QUILT = Project(ORG, BUCKET, PROJECT)

#PKG_3G=f"{PROJECT}/3g-devices"
#sg = QUILT.package(PKG_3G)

def save_ext(sg, dfs, key, ext):
    if ext == "report":
        return sg.export(dfs, key)
    elif ext == "table":
        return save_table(dfs[key], key)
    elif ext == "series":
        return save_table(dfs[key], key, "append")
    return sg.save_file(dfs[key], f'{key}.{ext}')

def cvm2quilt(cvm, name):
    pkg = f"{PROJECT}/{name}"
    if cvm.debug == True:
         pkg = pkg + "-debug"
    print("cvm2quilt package: "+pkg)
    sg = QUILT.package(pkg)

    doc = cvm.key_actions('doc')
    doc["cvm.actions"] = cvm.actions
    sg.save_dict(cvm.actions, name)
    msg = "Auto-generated from CQML"
    files = cvm.saveable()
    for key in files:
        ext = files[key]
        msg = save_ext(sg, cvm.df, key, ext)
    try:
        sg.copy_file(f'{name}.md','README.md')
        sg.copy_file(f'REPORT_HELP.md')
    except FileNotFoundError as err:
        print(err)
        #cvm.log(err)
    return sg.cleanup(msg, doc)

def setup_tables(spark, db, dict):
    spark.catalog.setCurrentDatabase(db)
    df = {}
    for key in dict:
      table_name = dict[key]
      dft = spark.table(table_name)
      print(f"{key}: {table_name}")
      df[key] = dft
    return df

NS_DB='netsuite_suiteanalytics'

def netsuite_tables(spark, dict):
    return setup_tables(spark, NS_DB, dict)

NS={
  "DP_ST": 'deployment_status',
  "NA_ST": 'nauto_account_statuses',
  "OT":'order_type',
  "IT":'items',
  "CUS": 'customers',
  "DL": 'nauto_deployment_lifecycle',
  "ISD": 'nauto_item_shipment_detail',
  "TRN": 'transactions',
}
