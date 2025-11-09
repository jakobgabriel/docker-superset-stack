## Datasource bundle (optional)

You can export connections + datasets from another Superset:

```bash
superset export_datasources -f datasources.zip
```

Put `datasources.zip` here or place a `datasources/` YAML tree, then run:

```bash
docker compose run --rm import_datasources
```

