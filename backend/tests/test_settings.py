from app.settings import Settings


def test_defaults_work_without_any_environment_variables():
    settings = Settings(_env_file=None)

    assert settings.vroom_url == "http://localhost:3000"
    assert settings.vroom_timeout == 30


def test_environment_variables_win(monkeypatch):
    monkeypatch.setenv("VROOM_URL", "http://vroom:3000")
    monkeypatch.setenv("VROOM_TIMEOUT", "5")

    settings = Settings(_env_file=None)

    assert settings.vroom_url == "http://vroom:3000"
    assert settings.vroom_timeout == 5

def test_reads_a_dotenv_file(monkeypatch, tmp_path):
    (tmp_path / ".env").write_text("VROOM_URL=http://from-dotenv:3000\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("VROOM_URL", raising=False)

    assert Settings().vroom_url == "http://from-dotenv:3000"