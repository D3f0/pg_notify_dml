# Postgres Notifications Example

Inspiration for this project comes from this
[blog post](https://coussej.github.io/2015/09/15/Listening-to-generic-JSON-notifications-from-PostgreSQL-in-Go/)
by Jeroen Coussement.

## How to run

```bash
docker-compose up --build
```

### Important pieces

* `services/postgres/docker-entrypoint-initdb.d/*.sql`

  Defines the table, function and sets the trigger. The
  channel name is a geric `events`
* `services/notifier/src/notifier/main.py`

  Simple script that connects to Postgres, adds an event listener
  whose callback is function printing to stdout.

* adminer

  This is a generic adminer image running in `:3000`. It should
  be reachable at [http://localhost:3000](http://localhost:3000/?pgsql=postgres&username=postgres&db=example&ns=public&select=products)

## In action

![](./docs/img/deepin-screen-recorder_Select%20area_20200726122102.gif)

