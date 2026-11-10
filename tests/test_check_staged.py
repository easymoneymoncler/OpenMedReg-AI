import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "check_staged", Path(__file__).resolve().parents[1] / "scripts" / "check_staged.py"
)
check_staged = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_staged)
violations = check_staged.violations


def test_plain_source_file_passes():
    assert violations("src/pipeline.py", b"print('ok')\n") == []


def test_private_corpus_is_blocked():
    assert violations("corpus/private/norme.txt", b"texte")


def test_client_data_is_blocked():
    assert violations("data/client/dossier.md", b"texte")


def test_gitkeep_in_private_dir_passes():
    assert violations("corpus/private/.gitkeep", b"") == []


def test_pdf_outside_allowed_dirs_is_blocked():
    assert violations("docs/norme.pdf", b"%PDF-1.7")


def test_pdf_in_public_corpus_passes():
    assert violations("corpus/public/mdr/reglement.pdf", b"%PDF-1.7") == []


def test_docx_in_eval_fixtures_passes():
    assert violations("eval/fixtures/dossier_fictif.docx", b"PK") == []


def test_standard_copyright_marker_is_blocked():
    text = "COPYRIGHT PROTECTED DOCUMENT\n" + "© ISO 2016\n"
    assert violations("notes/extrait.md", text.encode("utf-8"))


def test_clause_number_and_title_pass():
    text = "ISO 14971, clause 5 : analyse du risque (texte non reproduit)\n"
    assert violations("docs/perimetre.md", text.encode("utf-8")) == []


def test_api_key_is_blocked():
    key = "sk-ant-" + "a" * 40
    assert violations("config/settings.yaml", f"key: {key}\n".encode())


def test_env_file_is_blocked():
    assert violations(".env", b"X=1\n")


def test_oversized_file_is_blocked():
    assert violations("eval/big.json", b"0" * (check_staged.MAX_BYTES + 1))
