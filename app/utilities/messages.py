
class Mail:

    @staticmethod
    def activation(username, otp):
        return "Hi %s! \n\nWelcome to the platform.\n Please use the OTP %s to activate your account.\n " \
                 "Please validate your account before 5mn" % (username, otp)
