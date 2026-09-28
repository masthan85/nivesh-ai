# ADR 001: Keep a modular monolith

Status: Accepted.

Nivara AI will remain a React frontend plus modular FastAPI backend while the product and provider contracts are still evolving. Premature microservices would increase deployment, security and observability complexity without an established scaling boundary. Domain services and provider interfaces should be structured so high-load capabilities can be separated later.
