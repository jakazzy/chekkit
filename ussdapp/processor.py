from rest_framework.response import Response

from product.models import ProductCode
from ussdapp.models import UssdRecord


class USSDProcessor(object):
    # Response Types
    INITIATION = 'Initiation'
    RESPONSE = 'Response'
    TIMEOUT = 'Timeout'
    RELEASE = 'Release'
    HUBTEL = 'Hubtel'

    # Client States
    WELCOME = 'welcome'
    PRODUCT_CODE = 'product_code'
    VERIFY_PRODUCT = 'verify_product'
    VERIFY_PRODUCT_MENU = 'verify_product_menu'
    FINISH = 'finish'
    LOCATION = 'location'
    COMPLAINT = 'complaint'
    FEEDBACK = 'feedback'

    def __init__(self, data):
        self.mobile = data.get('Mobile')
        self.session_id = data.get('SessionId')
        self.service_code = data.get('ServiceCode')
        self.response_type = data.get('Type')
        self.message = data.get('Message')
        self.operator = data.get('Operator')
        self.sequence = data.get('Sequence')
        self.client_state = data.get('ClientState')
        self.gateway = self.HUBTEL
        self.record = self.record_session(data=data)

    def process_request(self):
        if self.response_type == self.INITIATION:
            return self.welcome_menu()

        elif self.response_type == self.RESPONSE:
            if self.client_state == self.VERIFY_PRODUCT_MENU:
                return self.verify_product_menu()

            elif self.client_state == self.VERIFY_PRODUCT:
                return self.verify_product()

            elif self.client_state == self.COMPLAINT:
                return self.complaint()

            elif self.client_state == self.FEEDBACK:
                return self.feedback()

            elif self.client_state == self.LOCATION:
                return self.enter_location()

            elif self.client_state == self.FINISH:
                return self.info_reward()

    def welcome_menu(self, error=False):
        error_text = 'Invalid Selection\n' if error else ''
        message = u'{}Welcome To Chekkit:\n\n1.Verify Product\n2.Exit'.format(error_text)
        return self.process_response(message=message, response_type=self.RESPONSE,
                                     client_state=self.VERIFY_PRODUCT_MENU)

    def verify_product_menu(self):
        if self.message == '1':
            return self.enter_product_code()
        elif self.message == '2':
            return self.exit_session()
        else:
            return self.welcome_menu(error=True)

    def enter_product_code(self, error=False):
        error_text = 'Invalid code, try again...\n' if error else ''
        message = u'{}Please enter product code:'.format(error_text)
        return self.process_response(message=message, response_type=self.RESPONSE, client_state=self.VERIFY_PRODUCT)

    def verify_product(self):
        if self.message:
            product_code = self.message
            try:
                if product_code.__len__() != 16:
                    return self.enter_product_code(error=True)
                int(product_code)
            except ValueError:
                return self.enter_product_code(error=True)

            try:
                product = ProductCode.objects.get(product_code=product_code)
                return self.verification_response(verified=True)
            except ProductCode.DoesNotExist or ValueError:
                return self.verification_response(verified=False)

        else:
            return self.enter_product_code(error=True)

    def verification_response(self, verified=True, error=False):
        error_text = 'Invalid input\n' if error else ''
        feedback_menu = '{}To claim your reward please choose a feedback option below:\n' \
                        '1. No feedback\n ' \
                        '2. Product was below quality\n ' \
                        '3. Product is too expensive' \
            .format(error_text)
        message = u'Congratulations, this product is an original! \n\n{}'.format(
            feedback_menu) if verified else u'Warning, this product is not an original! \nPlease enter location of purchase:\n'
        if verified:
            """
            Subsequent transaction after verifying that a product is original
            """
            return self.process_response(message=message, response_type=self.RESPONSE, client_state=self.FEEDBACK)
        else:
            """
            Subsequent transaction after verifying that a product is fake
            """
            return self.process_response(message=message, response_type=self.RESPONSE, client_state=self.COMPLAINT)

    def feedback(self, error=False):
        if self.message in ['1', '2', '3', '4']:
            ussd_record = self.get_ussd_record()
            ussd_record.complaint = self.message
            ussd_record.save()
            return self.enter_location(error=True)
        else:
            return self.verification_response(verified=True, error=True)

    def complaint(self, error=False):
        if self.message:
            ussd_record = self.get_ussd_record()
            ussd_record.complaint = self.message
            ussd_record.save()
            return self.exit_session()
        else:
            return self.enter_location(error=True)

    def enter_location(self, error=False):
        message = u'Please enter your location:'
        return self.process_response(message=message, response_type=self.RESPONSE, client_state=self.LOCATION)

    def info_reward(self):
        ussd_record = self.get_ussd_record()
        ussd_record.location = self.message
        ussd_record.save()
        message = u'Awesome your account has been credited with GHC 2.\nThank you'
        return self.process_response(message=message,
                                     client_state=self.FINISH, response_type=self.RELEASE)

    def process_response(self, message, response_type, client_state):
        response_dict = dict(Message=message, ClientState=client_state, Type=response_type)
        return Response(response_dict)

    def record_session(self, data):
        try:
            session = UssdRecord.objects.get(session_id=self.session_id)
            session.data = data
            session.save()
            return session
        except UssdRecord.DoesNotExist:
            session = UssdRecord.objects.create(session_id=self.session_id, mobile=self.mobile,
                                                gateway=self.gateway, data=data)
            return session

    def exit_session(self):
        message = u'Thank You'
        return self.process_response(message=message, client_state=self.FINISH, response_type=self.RELEASE)

    def get_ussd_record(self):
        try:
            return UssdRecord.objects.get(session_id=self.session_id)
        except Exception as e:
            return None
