## Database setup

### Docker command
```shell
docker container run --name eventboard --publish 5432:5432 -e POSTGRES_PASSWORD=<password> -e POSTGRES_USER=leaf -e POSTGRES_DB=datamart -d postgres:18.0
```

### Migrations

#### Create a new migration

Create schema command:
```shell
migrate create -ext sql schema-<snake-case-schema-name>
```

Create table command:
```shell
migrate create -ext sql table-<snake-case-table-name>
```

#### Migrate UP
- `cd` to migrations directory.
Command: `migrate -database "postgres://<user>:<password>@localhost:5432/<database>?sslmode=disable" -source file://. up`

#### Migrate Down 
- `cd` to migrations directory.
Command: `migrate -database "postgres://<user>:<password>@localhost:5432/<database>?sslmode=disable" -source file://. down`
