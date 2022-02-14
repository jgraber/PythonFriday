import sys

def test_a_temp_fileA(tmpdir):
    print(f"\nA: {tmpdir}")

def test_a_temp_fileB(tmp_path):
    print(f"\nB: {tmp_path}")   

def test_a_temp_fileC(tmpdir):
    print(f"\nC: {tmpdir}")


def test_collected_output(capsys):
    print("Hello world")
    captured = capsys.readouterr()
    assert "Hello world\n" == captured.out


def test_collected_errors(capsys):
    sys.stderr.write("ERROR")
    captured = capsys.readouterr()
    assert "ERROR" == captured.err

def test_use_fixture(request):
    print(f'found: {request.session.testscollected}')
    print(f'failed: {request.session.testsfailed}')