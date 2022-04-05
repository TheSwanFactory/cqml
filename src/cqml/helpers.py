#
# Utility Functions
#

from .keys import *

def mock_functions():
    from collections import namedtuple
    keys = "lit,col,desc,expr,sum,min,max,count,alias,concat_ws,current_date,current_time,current_timestamp,countDistinct,orderBy,over,partitionBy,row_number".split(',')
    func = namedtuple("Func",keys)
    f1 = func(*keys)
    l1 = [lambda *args, **kw: getattr(f1,key) for key in keys]
    f2 = func(*l1)
    l2 = [lambda *args, **kw: f2] * len(keys)
    return func(*l2)

try:
    from pyspark.sql.window import Window
    import pyspark.sql.functions as f
    f.col('f')
except AttributeError:
    f = mock_functions()
    Window = mock_functions()
    MOCK=True

def alias_columns(df, columns, table='.'):
    new_columns = []
    for col in columns:
        split = col.split(cAlias)
        col_name = split[0]
        alias_name = split[1] if len(split) > 1 else col_name
        meta = None if col_name == alias_name else { 'comment': f'WAS[{table}.{col_name}]' }
        entry = df[col_name].alias(alias_name,metadata=meta)
        new_columns.append(entry)
    return new_columns

def call_sql(action, args):
    sep = action[kOp] if kOp in action else ","
    sql = sep.join(map(str, args))
    if kFunc in action: sql = f'{action[kFunc]}({sql})'
    if kRound in action: sql = f'round({sql}, {action[kRound]})'
    if kIfNull in action: sql = f'coalesce({sql}, {action[kIfNull]})'
    return sql

def cast_columns(df, matching, type):
    for c in df.columns:
        if matching.lower() in c.lower():
            #print(f.col(c))
            df = df.withColumn(c, f.col(c).cast(type))
    return df

def drop_column(df, col):
    try:
        return df.drop(col)
    except AnalysisException:
        return df

def drop_table(spark, id):
    spark.sql(f'drop table if exists {DB}.{id}')

def find_exts(ext):
    if isinstance(ext, list): return ext
    if ext == "report": return "daily,grid".split(',')
    return [ext]

def flag2sql(action):
    where = action[kWhere]
    condition = make_expr(where)
    action[kSQL] =f"CASE WHEN {condition} THEN true END"
    return action

def get_cols(action, df):
    return list(action[kCols].keys()) if kCols in action else df.columns

def get_sort(action):
    if not kSort in action: return []
    s = action[kSort]
    if isinstance(s, list): return s
    if isinstance(s, dict): return list(s.keys())
    return [s]

def make_list(col): return list([row[0] for row in col.collect()])

def make_aggregates(agg):
  aggs = []
  for field in agg:
    relation = agg[field]
    method = getattr(f, relation)
    col = method(field)
    meta = { 'comment': f'{field}: {relation}' }
    alias = f'n_{field}' if relation == 'count' else f'{relation}_{field}'
    name = col.alias(alias, metadata=meta)
    aggs.append(name)
  return aggs

def make_any(field, sub_query):
    any_expr = [sql_expr(field, op, value) for value, op in sub_query.items()]
    return f'({" OR ".join(any_expr)})'

def make_expr(query, op="AND"):
    field_expr = [make_any(field, query[field]) for field in query.keys()]
    return f" {op} ".join(field_expr)

def make_isin(query):
    field_expr = [make_any(field, query[field]) for field in query.keys()]
    return " AND ".join(field_expr)

def join_col(cols, join_into):
    n_joins = len(join_into)
    join_from = cols[:n_joins]
    #del cols[:n_joins]
    dupe = set(join_into) & set(join_from)
    jfmap = {d: f'JOIN:{d}' for d in list(dupe)}
    jf2 = [jfmap[j] if j in jfmap else j for j in join_from]
    joins = list(zip(join_into, jf2))
    print('join_col.alias')
    print(jfmap)
    return {
        "alias": jfmap,
        "zip": joins,
        "into": join_into,
        "from": jf2,
        "cols": cols,
    }

def keep(df, action, j):
    """
    If overlapping names in Left and Right,
    AND (only) one of those names is being dropped,
    THEN we need to rewrite the one being dropped
    """
    isInner = j["how"] == kInner
    ji = j["into"]
    jf = j["from"]

    if kKeepJoin not in action:
        return df.drop(*jf) if isInner else df.drop(*jf, *ji)
    keep = action[kKeepJoin]
    if keep == 'left':
        return df.drop(*jf)
    elif keep == 'right':
        return df.drop(*ji)
    return df

def join_expr(df_into, df_from, joins):
  df2 = rename_columns(df_from, joins['alias'])
  print('join_expr.df2')
  print(df2)
  joins["df_i"] = df_into
  joins["df_f"] = df2
  joins["expr"] = join_item(df_into, df2, joins["zip"][0])
  return joins

def join_item(df_into, df_from, item):
  key_into = item[0]
  key_from = item[1]
  if cAlias in key_from:
      key_from = key_from.split(cAlias)[1]
  expression = (df_into[key_into] == df_from[key_from])
  return expression

# https://stackoverflow.com/questions/38798567/pyspark-rename-more-than-one-column-using-withcolumnrenamed

def rename_columns(df, columns):
    if isinstance(columns, dict):
        return df.select(*[f.col(c).alias(columns.get(c, c)) for c in df.columns])
    else:
        raise ValueError("'columns' should be a dict, like {'old1':'new1', 'old2':'new2'}")

def sql_expr(field, op, value):
  if op == "contains":
    return f"({field} LIKE '%{value}%')"
  if op == "equals":
    return f"case {field} when {value} then true else null end"
  if op == "greater":
    return f"({field} > {value})"
  if op == "lesser":
    return f"({field} < {value})"
  if op == "notgreater":
    return f"({field} <= {value})"
  if op == "notlesser":
    return f"({field} >= {value})"
  if op == "not_contains":
    return f"({field} NOT LIKE '%{value}%')"
  if op == "is_not":
    return f"({field} IS NOT NULL)"
  if op == "is":
    return f"({field} IS NULL)"
  return f"sql_expr: ERROR Unknown operator {op}"

def summarize(df, table, col, count, now):
    dc = df.groupby(col).agg(f.countDistinct(count))
    dsum = dc.select(
      f.lit(table).alias('table'),
      f.lit(col).alias('column'),
      f.col(col).alias('value'),
      f.col(f'count({count})').alias('count'),
      f.current_date().alias('date'),
      f.lit(now).alias('timestamp'),
    )
    return dsum.orderBy('value')

def unique(df_from, sort, cols):
    N = "windowIndx"
    col = f.desc(sort) #if kReverse else f.asc(sort)
    win = Window.partitionBy(cols).orderBy(col)
    df_win = df_from.withColumn(N,f.row_number().over(win))
    df_dupes = df_win.filter(f.col(N) != 1).drop(N)
    #self.save("DUPE_"+id, df_dupes, "csv")
    df = df_win.filter(f.col(N) == 1).drop(N)
    return df
