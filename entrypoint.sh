#!/bin/bash
# Wait for the database before running setup.py and starting streamlit

# Check database connection
until pg_isready -h db -p 5432 -U leistungs_user; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Run setup.py
python setup.py

# Start Streamlit
streamlit run main.py --server.port 8502
