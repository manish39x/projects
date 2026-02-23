docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="nhl_stats" \
  -v nhl_stats_postgres_data:/var/lib/postgresql \
  -p 5433:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18
  