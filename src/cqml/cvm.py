from copy import deepcopy
from functools import reduce
from operator import itemgetter
from .keys import *
from .helpers import *
from .vm import VM

try:
    import pyspark.sql.functions as f
    f.col('f')
except AttributeError:
    f = mock_functions()

HAS_TEMPO=True
try:
  from tempo import TSDF
except ImportError:
  HAS_TEMPO=False
  pass

from boxsdk import OAuth2, Client
from .boxquilt import BoxQuilt

class CVM(VM):
    def __init__(self, yaml, spark):
        super().__init__(yaml, spark)

    def do_assign(self, action):
        id, from_key = itemgetter('id','from')(action)
        df_from = self.get_frame(from_key)
        return df_from

    def do_box(self, action):
        print('do_box')
        from_key, group, config = itemgetter('from','group','box')(action)
        df_from = self.get_frame(from_key)
        sort = action[kSort] if kSort in action else [group]
        self.log('do_box: init')
        bq = BoxQuilt(group, sort, self, config)
        self.log('do_box: save_groups')
        bq.save_groups(df_from, kSkipSave in action) #
        self.log('do_box: load_groups')
        bq.load_groups()
        self.log('do_box: create_or_update_box')
        bq.create_or_update_box(kSkipUpload in action) #
        self.log('do_box: box_table')
        df = bq.box_table()
        return df

    def do_calc(self, action):
        id, from_key,args,cdict = itemgetter('id','from','args',kCols)(action)
        df_from = self.get_frame(from_key)
        i = args.index(kColArg)
        result = ['*']
        for col, alias in cdict.items():
            args[i] = col
            sql = call_sql(action, args)
            expr = f'{sql} as {alias}'
            result.append(expr)
        all = ",".join(result)
        self.log(' - do_calc.all: '+all)
        df_from.createOrReplaceTempView(id)
        select = f"select {all} from {id}"
        return self.spark.sql(select)

    def do_call(self, action):
        args  = action[kArgs]
        sql = call_sql(action, args)
        action[kSQL] = sql
        return self.do_eval(action)

    def do_eval(self, action):
        id, from_key, sql = itemgetter('id','from',kSQL)(action)
        df_from = self.get_frame(from_key)
        self.log(' - do_eval: '+sql)
        meta = { 'comment': f'{id}: {sql}' }
        df = df_from.withColumn(id, f.expr(sql))
        return df

    def do_flag(self, action):
        sql_action = flag2sql(action)
        return self.do_eval(sql_action)

    # TODO: Optimize creating multiple columns
    def do_flags(self, action):
        """
        url='https://stackoverflow.com/questions/41400504/spark-scala-repeated-calls-to-withcolumn-using-the-same-function-on-multiple-c/41400588#41400588'
        window = Window.partitionBy("ID").orderBy("time")
        df.select(
            "*", # selects all existing columns
            *[
                F.sum(col).over(windowval).alias(col_name)
                for col, col_name in zip(["A", "B", "C"], ["cumA", "cumB", "cumC"])
            ]
        )
        expr_map = {f['id']: flag2sql(f)[kSQL] for f in flags}
        df = createColumns(df, expr_map)
        """

        from_key,flags = itemgetter('from','flags')(action)
        df = self.get_frame(from_key)
        for faction in flags:
            print(faction)
            sql_action = flag2sql(faction)
            id, sql = itemgetter('id',kSQL)(sql_action)
            self.log(sql)
            df = df.withColumn(id, f.expr(sql))
        return df

    def do_group(self, action):
        from_key,agg = itemgetter('from','agg')(action)
        df_from = self.get_frame(from_key)
        aggs = make_aggregates(agg)
        cols = get_cols(action, df_from)
        df = df_from.groupby(*cols).agg(*aggs)
        name = '_'.join(cols)
        df = df.withColumn(name, f.concat_ws(".", *cols))
        return df

    def do_latest(self, action, latest=True):
        name, tables = itemgetter('id', 'tables')(action)
        id = name.split('.')[0] if "." in name else name
        self.spark.catalog.setCurrentDatabase(id)
        group = [DATE_UNIQ] if kCols not in action else get_cols(action, None)
        for key in tables:
          if key not in self.df:
              table_name = tables[key]
              df = self.spark.table(table_name)
              if latest:
                  df = unique(df, DATE_COL, group)
              print(f" - {key}: {table_name}")
              self.set_frame(key, df)
        return self.df

    def do_load(self, action):
        df = self.do_latest(action, False)
        return df

    def do_loadfiles(self, action):
        folder, files = itemgetter('id', 'tables')(action)
        for key in files:
          file_name = files[key]
          path = f"file:{folder}/{file_name}"
          df = self.spark.read.format("csv").option("header","true").load(path)
          print(f" - {key}[{file_name}]: {path}")
          df = cast_columns(df, action[kCast], "int") if kCast in action else df
          self.set_frame(key, df)
        return self.df

    def do_merge(self, action):
        id, into, join = itemgetter('id', 'into', 'join')(action)
        df_into = self.get_frame(into)
        df_from = self.do_select(action, False) # do not auto-sort on join column
        cols = get_cols(action, df_from)
        #if not df_from: return None
        join_into = join if isinstance(join, list) else [join]
        joins = join_col(cols, join_into)
        joins = join_expr(df_into, df_from, joins)
        joins["how"] = action[kJoinType] if kJoinType in action else 'left'
        self.log(joins, 'joins')
        df = df_into.join(joins['df_f'], joins['expr'], joins["how"])
        df = keep(df, action, joins)
        return df

    def do_pivot(self, action):
        from_key, agg, pivot = itemgetter('from','agg','pivot')(action)
        df_from = self.get_frame(from_key)
        aggs = make_aggregates(agg)
        cols = get_cols(action, df_from)
        df = df_from.groupby(*cols).pivot(pivot).agg(*aggs)
        df = df.withColumn(action['id']+"_pkey", f.concat_ws(".", *cols))
        return df

    def do_rebin(self, action):
        values = action['values']
        clauses = []
        for value in values:
          condition = make_expr(values[value])
          sql = f"WHEN {condition} THEN '{value}'" # value must be a literal
          clauses.append(sql)
        action[kSQL] =f"CASE {' '.join(clauses)} END"
        return self.do_eval(action)

    def do_resample(self, action):
        from_key,ts,freq,func = itemgetter('from','time','freq','func')(action)
        cols = get_cols(action, df_from)
        df_from = self.get_frame(from_key)
        df_ts = TSDF(df_from,ts_col=ts,partition_cols=cols)
        df_re = df_ts.resample(freq=freq, func=func, fill=True)#.interpolate(method="linear")
        return df_re.df

    def do_select(self, action, autoSort=True):
        from_key = itemgetter('from')(action)
        df = self.get_frame(from_key)
        cols = get_cols(action, df)
        if (kSort not in action) and autoSort:
            value = cols[0]
            action[kSort] = value.split(cAlias)[1] if cAlias in value else value
        if kWhere in action:
            expression = make_expr(action[kWhere])
            self.log(f' - do_select[{kWhere}]: '+expression)
            df = df.filter(expression)
        if kAny in action:
            expression = make_expr(action[kAny], "OR")
            self.log(f' - do_select[{kAny}]: '+expression)
            df = df.filter(expression)
        if kMatch in action:
            for col, dict in action[kMatch].items():
                for table, tcol in dict.items():
                    self.log(f' - do_select[{kMatch}]: ({col}).leftsemi({table},{tcol})')
                    dft = self.get_frame(table)
                    df = df.join(dft, df[col] == dft[tcol], "leftsemi")
        if 'dedupe' in action:
            df = df.drop_duplicates([action['dedupe']])
        column_map = alias_columns(df, cols, from_key)
        df = df.select(*column_map)
        return df

    def do_summary(self, action):
        from_key = action['from']
        df_from = self.get_frame(from_key)
        cols = get_cols(action, df_from)
        count = action['count']
        now = None
        now = f.current_timestamp()
        id = self.get_key(from_key)
        sums = [summarize(df_from, id, col, count, now) for col in cols]
        df = reduce(lambda x, y: x.union(y), sums)
        return df

    def do_union(self, action):
        id, fkey, ikey = itemgetter('id', 'from', 'into')(action)
        df_from = self.get_frame(fkey)
        df_into = self.get_frame(ikey)
        if kDrop in action:
            df_from = df_from.drop(*action[kDrop])
        return df_from.union(df_into)

    def do_unique(self, action):
        N = "windowIndx"
        id, key, sort = itemgetter('id', 'from', kSort)(action)
        df_from = self.get_frame(key)
        cols = get_cols(action, df_from)
        df = unique(df_from, sort, cols)
        return df

    def do_update(self, action):
        id, from_key, join = itemgetter('id','from','join')(action)
        old = self.spark.table(f'{DB}.{id}')
        new = self.get_frame(from_key)
        for c in new.columns:
            if c != join:
                old = drop_column(old, c)
        df = old.join(new, join)
        return df
