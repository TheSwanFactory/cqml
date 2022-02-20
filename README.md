# cqml
Composable Query Meta Language

CQML is declarative data format for specifying complete data analysis pipelines.  It is most commonly implemented as YAML, but can trivially be transformed into JSON, CSON, or macOS and Java property lists.

The initial back-end is written for the DataBrick's flavor of PySpark and Spark SQL, but should be easy to extend to other databases and warehouses.

# USAGE
```
import cqml
```

# Building the Packages

```
$ python3 -m pip install --upgrade build
$ python3 -m build
$ python3 -m pip install --upgrade twine
$ python3 -m twine dist/*
```
