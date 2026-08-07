from incident_management.runbook_generator.src.utils.file_utils import read_text_file, write_text_file

def test_write_and_read_text_file(tmp_path):
    """
    Verify that text written to a file can be read back successfully.
    """
    file_path = tmp_path/"text.txt"
    content = "Hello World"

    write_text_file(
        str(file_path),
        content
    )

    assert file_path.exists()
    assert read_text_file(str(file_path)) == "Hello World"