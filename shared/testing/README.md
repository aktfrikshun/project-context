<!-- Purpose: Defines shared verification principles and evidence expectations. -->
# Testing

- Test behavior at the cheapest level that gives reliable evidence.
- Prioritize business rules, public contracts, security boundaries, failure modes, and data migrations.
- Keep tests deterministic, isolated, readable, and meaningful when they fail.
- Use production-like integration tests where mocks would hide contract risk.
- Document test data privacy and lifecycle.
- Define release gates and ownership for quarantined tests.
- Record manual verification when automation is disproportionate, including date and evidence.

Each project should document its test layers, commands, environments, quality gates, and known gaps in `conventions.md` or a linked project document.
