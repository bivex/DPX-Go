package query

type Query struct {
	table  string
	fields []string
	where  string
	limit  int
}

type QueryBuilder struct {
	query Query
}

func NewQueryBuilder(table string) *QueryBuilder {
	return &QueryBuilder{
		query: Query{table: table},
	}
}

func (b *QueryBuilder) Select(fields ...string) *QueryBuilder {
	b.query.fields = fields
	return b
}

func (b *QueryBuilder) Where(condition string) *QueryBuilder {
	b.query.where = condition
	return b
}

func (b *QueryBuilder) Limit(limit int) *QueryBuilder {
	b.query.limit = limit
	return b
}

func (b *QueryBuilder) Build() (Query, error) {
	return b.query, nil
}
