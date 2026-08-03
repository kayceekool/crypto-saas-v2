# Release Notes

## V3 Package 01

Package 01 is the Core Runtime Foundation.

### Definition of Done

- FastAPI application imports
- Runtime starts through FastAPI lifespan
- SQLite database initializes asynchronously
- Scheduler starts and stops cleanly
- Health endpoint reports runtime components
- Metrics endpoint reports runtime counters
- Provider registry is available
- Initial runtime tests are available

### Safety

No live trading or transaction execution is included in this package.