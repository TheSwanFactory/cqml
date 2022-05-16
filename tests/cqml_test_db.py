# Databricks notebook source
# MAGIC %md
# MAGIC # CQML
# MAGIC ## Compact Query Meta Language
# MAGIC ### Databricks Test Notebook

# COMMAND ----------

!pip install --upgrade pip
#!pip install cqml
!pip --no-cache-dir install git+https://github.com/TheSwanFactory/cqml.git@convert45
!pip install cqml==0.5.0.dev12

import cqml

# COMMAND ----------

CQML_ROOT="../pipes"
root = cqml.Root(CQML_ROOT)
keys = root.keys()
print(f'{root.root}: {root.env}')
dbutils.widgets.dropdown("CONF", keys[0], keys)
dbutils.widgets.dropdown("DEBUG", "DEBUG", ["DEBUG", "PROD"])

# COMMAND ----------

CONF=getArgument("CONF")
DEBUG=True if getArgument("DEBUG") == "DEBUG" else False
print(f'Parameters[{CONF}]DEBUG={DEBUG}')
cvm = root.new(spark, CONF, DEBUG)
print(cvm.yaml['env'])

# COMMAND ----------

#if not DEBUG:
cvm.run()
print(cvm.sizes)
dbutils.notebook.exit(0)

# COMMAND ----------

cvm.init()
steps = cvm.steps()
print(steps)
#dbutils.notebook.exit(0)


# COMMAND ----------

df = {}
def values(s, col): return df[s].select(col).distinct().collect()

for step in steps:
    print(step)
    df[step] = cvm.test(step)
    df[step].show()

# COMMAND ----------

cvm.save()
displayHTML(cvm.result())

# COMMAND ----------

dbutils.notebook.exit(0)
#spark.sql('create database nauto')

# COMMAND ----------

#spark.sql('drop table if exists default.3g_devices_superfleet')
