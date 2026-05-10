from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_milestone_04_summary_documents_current_contracts():
    text = read_text("docs/MILESTONE_04_SUMMARY.md")

    assert "Documentation Milestone 04" in text
    assert "Static UI polish and read-only operator usability" in text
    assert "Read-only API payload consistency pass" in text
    assert "Redaction policy coverage expansion" in text
    assert "selfdev.read_api.payload.v1" in text
    assert "RedactionResult" in text
    assert "HTTP API and static UI remain read-only" in text


def test_required_docs_include_milestone_04_markers():
    for rel in [
        "README.md",
        "CHANGELOG.md",
        "docs/IMPLEMENTATION_STATUS.md",
        "docs/DEV_PLAN_SHORT_TERM.md",
        "docs/SPECIFICATION.md",
        "docs/TEST_PLAN.md",
    ]:
        text = read_text(rel)
        assert "SELFDEV:MILESTONE_04_START" in text
        assert "SELFDEV:MILESTONE_04_END" in text


def test_milestone_04_test_plan_keeps_full_contract_suite_command():
    text = read_text("docs/TEST_PLAN.md")
    assert "python scripts/selfdev/run_contract_tests.py" in text
    assert "test_read_api_payload_consistency.py" in text
    assert "test_redaction_policy_coverage.py" in text
