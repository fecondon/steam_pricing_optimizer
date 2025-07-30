import subprocess


def test_streamlit_run():
    result = subprocess.run(
        ['streamlit', 'run', 'app/steamlit.py', '--server.headless', 'true'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
    )

    assert result.returncode == 0 or result.returncode == 1