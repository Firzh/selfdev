from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DOCS = [
    ROOT / "README.md",
    ROOT / "CHANGELOG.md",
    ROOT / "docs" / "IMPLEMENTATION_STATUS.md",
    ROOT / "docs" / "DEV_PLAN_SHORT_TERM.md",
    ROOT / "docs" / "SPECIFICATION.md",
    ROOT / "docs" / "TEST_PLAN.md",
    ROOT / "docs" / "MILESTONE_03_SUMMARY.md",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_milestone_03_required_docs_exist_and_are_non_empty():
    for path in REQUIRED_DOCS:
        assert path.exists(), path
        assert read(path).strip(), path


def test_milestone_03_docs_record_current_cycle():
    summary = read(ROOT / "docs" / "MILESTONE_03_SUMMARY.md")
    assert "Documentation Milestone 03" in summary
    assert "Minimal UI Static Console" in summary
    assert "UI static file server route" in summary
    assert "Target registry read API" in summary
    assert "Artifact viewer read API" in summary
    assert "Redaction service skeleton" in summary
    assert "Redacted artifact preview read API" in summary
    assert "UI root asset path fix" in summary


def test_milestone_03_docs_list_current_read_only_endpoints():
    combined = "\n".join(read(path) for path in REQUIRED_DOCS)
    expected = [
        "GET /ui",
        "GET /targets",
        "GET /targets/{target_id}",
        "GET /artifacts/{artifact_id}",
        "GET /artifact-previews/{artifact_id}",
        "GET /actions/{task_id}",
    ]
    for endpoint in expected:
        assert endpoint in combined


def test_milestone_03_docs_keep_safety_boundary_explicit():
    combined = "\n".join(read(path) for path in REQUIRED_DOCS)
    assert "No LLM" in combined
    assert "No shell execution" in combined or "execute shell" in combined
    assert "No patch application" in combined or "apply patch" in combined
    assert "No write API" in combined or "read-only API" in combined
    assert "POST" in combined and "PUT" in combined and "DELETE" in combined


def test_milestone_03_docs_define_next_feature_scope():
    plan = read(ROOT / "docs" / "DEV_PLAN_SHORT_TERM.md")
    assert "Goal 28: Static UI polish and read-only operator usability" in plan
    assert "framework-free" in plan
    assert "no mutation controls" in plan
