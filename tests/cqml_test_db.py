# Databricks notebook source
# MAGIC %md
# MAGIC # 3G Sunset - Master Devices Report
# MAGIC ## Debugging Notebook

# COMMAND ----------

!python -m pip install --upgrade pip
#!pip install cqml
!pip --no-cache-dir install git+https://github.com/TheSwanFactory/cqml.git@v32-reframe
!pip install cqml==0.3.2.dev2
import cqml

# COMMAND ----------
KEY="cqml_test"
#dict = cqml.pkg_all(spark, 'pipes')
#dict = cqml.pkg_cqml(KEYS[6],spark, 'pipes')
cvm = cqml.load_cqml(KEY,spark, '.')
cvm.debug = True
cvm.run()

# COMMAND ----------

dict = cvm.do_save({})

# COMMAND ----------

displayHTML(dict['html'])
#dict

# COMMAND ----------

#spark.sql('create database nauto')

# COMMAND ----------

#spark.sql('drop table if exists default.3g_devices_superfleet')
