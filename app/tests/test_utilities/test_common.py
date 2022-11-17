import pytest
from app.utilities.common import *


@pytest.mark.unitest
class Test_generate_token:

    def test_no_param_should_return_default_length(self):
        otp = generate_token()

        assert len(otp) == 5

    def test_should_return_digits(self):
        otp = generate_token()

        assert isinstance(int(otp), int) is True

    @pytest.mark.parametrize('otp_length', [5, 6, 9])
    def test_with_param_should_return_same_length(self, otp_length):
        otp = generate_token(otp_length)

        assert len(otp) == otp_length


# @pytest.mark.unitest
# class Test_Mail:
#
#     def test_mail(self, mocker):
#         mocker.patch('utilities.common.send_mail', return_value=False)
#         assert mail("ddd", ["ssss"], "ddd") is False

