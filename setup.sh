#!/bin/bash

# Auth0 Setup
export AUTH0_DOMAIN='dev-awp6mkwgqzczsw4w.us.auth0.com'
export AUTH0_CLIENT_ID='YVn5O30tzovUnhAZ9G2pfIqg6DwT1qzV'
export API_AUDIENCE='dev'
export JWT_SECRET=''  # Only if needed for local JWT verification

# Database
export DATABASE_URL="postgresql+psycopg://postgres:abcdefgh@localhost:5432/agency"

echo "Environment variables set!"
