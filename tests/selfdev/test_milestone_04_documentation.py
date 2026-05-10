from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_milestone_04_summary_documents_current_contracts():
    summary = read("docs/MILESTONE_04_SUMMARY.md")

    assert "Milestone 04 Summary" in summary
    assert "Completed Since Documentation Milestone 03" in summary
    assert "selfdev.read_api.payload.v1" in summary
    assert "RedactionResult" in summary
    assert "Next Work" in summary
    assert "not a fixed feature-commit count" in summary


def test_implementation_status_is_synced_to_milestone_04():
    status = read("docs/IMPLEMENTATION_STATUS.md")

    assert "Documentation Milestone 04 Status" in status
    assert "Milestone: Documentation Milestone 04" in status
    assert "Completed Since Documentation Milestone 03" in status
    assert "Stable Contracts" in status
    assert "Next Work Candidates" in status
    assert "Documentation Milestone 02 completed" not in status
    assert "Phase 27: Documentation Milestone 03 In progress" not in status


def test_milestone_04_docs_avoid_hard_coded_feature_commit_count():
    docs = chr(10).join(
        [
            read("README.md"),
            read("CHANGELOG.md"),
            read("docs/IMPLEMENTATION_STATUS.md"),
            read("docs/MILESTONE_04_SUMMARY.md"),
            read("docs/DEV_PLAN_SHORT_TERM.md"),
        ]
    ).lower()

    forbidden = (
        "9 " + "feat",
        "nine " + "feat",
        "9 " + "feature " + "commit",
        "nine " + "feature " + "commit",
        "9 " + "implementation " + "commit",
        "nine " + "implementation " + "commit",
    )
    assert not any(phrase in docs for phrase in forbidden)


def test_read_api_and_redaction_contracts_are_documented():
    combined = chr(10).join(
        [
            read("README.md"),
            read("docs/SPECIFICATION.md"),
            read("docs/TEST_PLAN.md"),
            read("CHANGELOG.md"),
        ]
    )

    assert "selfdev.read_api.payload.v1" in combined
    assert "Read API Payload Contract" in combined
    assert "RedactionResult" in combined
    assert "Redaction policy coverage expansion" in combined
