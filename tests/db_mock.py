# Mock DataBricks spark API for testing
from copy import deepcopy

class MockBox(object):
    def __init__(self):
        self.name = "MockBox.name"
        self.id = "MockBox.id"
    def folder(self, arg): return self
    def get_items(self): return [self]

class MockCol(object):
    def __init__(self, name): self.name = name
    def alias(self, name,metadata={"meta":"data"}): return name
    def contains(self, value): return True
    def desc(self): return True

class MockWriter(object):
    def __init__(self, df): self.df = df
    def csv(self, arg): return self
    def format(self, arg): return self
    def load(self, arg): return MockFrame(arg)
    def mode(self, arg): return self
    def option(self, *arg): return self
    def partitionBy(self, *arg): return self
    def parquet(self, arg): return self
    def saveAsTable(self, arg): return self

class MockFrame(object):
    def __init__(self, name="frame"):
        self.name = name
        self.items = {}
        self.columns = []
        self.write = MockWriter(self)

    def __getitem__(self, item):
        return self.items[item] if item in self.items else MockCol(item)

    def select(self, *input):
        if input[0] == 'row_number': return self
        dup =  deepcopy(self)
        columns = list(input.values()) if isinstance(input, dict) else input
        dup.columns = columns
        for col in columns:
            mcol = MockCol(col)
            setattr(dup, col, mcol)
            dup.items[col] = mcol
        return dup

    def drop(self, *col):
        try:
            cols = list(self.columns)
            cols.remove(col)
            self.columns = cols
        except ValueError: skipped = True
        return self

    def agg(self, *aggs): return self
    def count(self): return 1
    def coalesce(self, arg): return self
    def distinct(self): return self
    def filter(self, arg): return self
    def groupby(self, *arg): return self
    def join(self, df_from, join, how): return deepcopy(df_from)
    def orderBy(self, arg): return self
    def pivot(self, arg): return self
    def createOrReplaceTempView(self, arg): return self
    def sort(self, *arg,**kwarg): return self
    def union(self, arg): return self
    def withColumn(self, *arg): return self

class MockSpark(object):
    def __init__(self): self.columns = []
    def createDataFrame(self, list): return self.table('list')
    def count(self): return self
    def distinct(self,arg=None): return self
    def get(self, arg): return f'mock.get:{arg}'
    def setCurrentDatabase(self, db): print(f"setCurrentDatabase: {db}")
    def sql(self, arg): return self
    def table(self, table_name): return MockFrame(table_name)

spark = MockSpark()
spark.catalog = spark#.setCurrentDatabase
spark.conf = spark#.setCurrentDatabase
spark.conf.client = MockBox()
spark.read = MockWriter(spark)
