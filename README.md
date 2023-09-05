# Postgres Notify Data Manipulation Language

This Python package allows to auto-create TRIGGERS that will generate
JSON updates of rows in the configured tables (defaults all) that will
be published though NOTIFY and LISTENed in your framework of choice. Initial
support is for FastAPI.

[Original Idea](./legacy/README.md)


## Development

### Running the tests

```bash
hatch run test
```
