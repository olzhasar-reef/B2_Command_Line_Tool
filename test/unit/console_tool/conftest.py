######################################################################
#
# File: test/unit/console_tool/conftest.py
#
# Copyright 2023 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################
import os
import sys
from test.unit.test_console_tool import BaseConsoleToolTest

import pytest


class ConsoleToolTester(BaseConsoleToolTest):
    def authorize(self):
        self._authorize_account()

    def run(self, *args, **kwargs):
        return self._run_command(*args, **kwargs)


@pytest.fixture
def b2_cli():
    cli_tester = ConsoleToolTester()
    cli_tester.setUp()
    yield cli_tester
    cli_tester.tearDown()


@pytest.fixture
def authorized_b2_cli(b2_cli):
    b2_cli.authorize()
    yield b2_cli


@pytest.fixture
def bucket_info(b2_cli, authorized_b2_cli):
    bucket_name = "my-bucket"
    bucket_id = "bucket_0"
    b2_cli.run(['create-bucket', bucket_name, 'allPublic'], expected_stdout=f'{bucket_id}\n')
    return {
        'bucketName': bucket_name,
        'bucketId': bucket_id,
    }


@pytest.fixture
def bucket(bucket_info):
    return bucket_info['bucketName']


@pytest.fixture
def mock_stdin(monkeypatch):
    out_, in_ = os.pipe()
    monkeypatch.setattr(sys, 'stdin', os.fdopen(out_))
    in_f = open(in_, 'w')
    yield in_f
    in_f.close()


@pytest.fixture
def local_file(tmp_path):
    """Set up a test file and return its path."""
    filename = 'file1.txt'
    content = 'hello world'
    local_file = tmp_path / filename
    local_file.write_text(content)

    mod_time = 1500111222
    os.utime(local_file, (mod_time, mod_time))

    return local_file


@pytest.fixture
def uploaded_file(b2_cli, bucket_info, local_file):
    filename = 'file1.txt'
    b2_cli.run(['upload-file', '--quiet', bucket_info["bucketName"], str(local_file), filename])
    return {
        'bucket': bucket_info["bucketName"],
        'bucketId': bucket_info["bucketId"],
        'fileName': filename,
        'fileId': '9999',
        'content': local_file.read_text(),
    }