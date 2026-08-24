package database

import (
	"sync"
)

type DBConnection struct {
	dsn string
}

var (
	dbInstance *DBConnection
	dbOnce     sync.Once
)

func GetDatabaseInstance() *DBConnection {
	dbOnce.Do(func() {
		dbInstance = &DBConnection{dsn: "postgres://localhost:5432/main"}
	})
	return dbInstance
}
