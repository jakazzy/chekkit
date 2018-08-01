from rest_framework import status
from rest_framework.response import Response

from product.models import ProductCode
from ussdapp.models import UssdRecord

INITIATION = 'Initiation'
RESPONSE = 'Response'
TIMEOUT = 'Timeout'
RELEASE = 'Release'
HUBTEL = 'Hubtel'

# client states
WELCOME = 'welcome'
PRODUCT_CODE = 'product_code'
VERIFY_PRODUCT = 'verify_product'
VERIFY_PRODUCT_MENU = 'verify_product_menu'
FINISH = 'finish'
LOCATION = 'location'
COMPLAINT = 'complaint'


class USSDProcessor(object):

    def __init__(self, data):
        self.phone_no = data.get('Mobile')
        self.session_id = data.get('SessionId')
        self.service_code = data.get('ServiceCode')
        self.stage = data.get('ClientState')
        self.response_type = data.get('Type')
        self.operator = data.get('Operator')
        self.message = data.get('Message')
        self.sequence = data.get('Sequence')
        self.gateway = HUBTEL
        self.record = self.record_session(data=data)

    def process_request(self):
        if self.response_type == INITIATION:
            return self.welcome_menu()

        elif self.response_type == RESPONSE:

            if self.stage == VERIFY_PRODUCT_MENU:
                return self.verify_product_menu()

            elif self.stage == VERIFY_PRODUCT:
                return self.verify_product()

            elif self.stage == COMPLAINT:
                return self.complaint()

            elif self.stage == LOCATION:
                return self.enter_location()

    def welcome_menu(self, error=False):
        error_text = 'Invalid Selection\n' if error else ''
        message = '{}\nWelcome To Chekkit\n\n1.Verify Product\n2.Exit'.format(error_text)
        return self.process_response(message=message, response_type=RESPONSE, client_state=VERIFY_PRODUCT_MENU)

    def verify_product_menu(self):
        if self.message == '1':
            return self.enter_product_code()
        elif self.message == '2':
            # TODO no exit_session was provided
            return self.exit_session()
        else:
            return self.welcome_menu(error=True)

    def enter_product_code(self, error=False):
        error_text = 'Please enter a valid product code\n' if error else ''
        message = '{}Please enter product code.'.format(error_text)
        return self.process_response(message=message, response_type=RESPONSE, client_state=VERIFY_PRODUCT)

    def verify_product(self):
        if self.message:
            product_code = self.message
            try:
                product = ProductCode.objects.get(product_code=product_code)
                return self.verification_response(verified=True)
            except ProductCode.DoesNotExist:
                return self.verification_response(verified=False)

        else:
            return self.enter_product_code(error=True)

    def verification_response(self, verified=True, error=False):
        error_text = 'Invalid input\n' if error else ''
        complaint_menu = '{}If you have any complaints please choose an option below:\n 1.No complaint\n 2.Product was below quality\n 3.Product is too expensive'.format(
            error_text)
        message = u'Congratulations, this product is an original! \n\n{}'.format(
            complaint_menu) if verified else u'Warning! the product is not original.\n{}'.format(complaint_menu)
        return self.process_response(message=message, response_type=RESPONSE, client_state=COMPLAINT)

    def complaint(self, error=False):
        if self.message in ['1', '2', '3', '4']:
            ussd_record = self.get_ussd_record()
            ussd_record.complaint = self.message
            ussd_record.save()
            return self.enter_location(error=True)
        else:
            return self.verification_response(error=True)

    def location(self):
        message = u'Please enter a location:'
        return self.process_response(message=message, response_type=RESPONSE, client_state=LOCATION)

    def enter_location(self, error=False):
        ussd_record = self.get_ussd_record()
        ussd_record.location = self.message
        ussd_record.save()
        return self.process_response(message='Awesome the account has been credited with Ghc.2\n Thank you',
                                     client_state=FINISH, response_type=RELEASE)

    def process_response(self, message, response_type, client_state):
        response_dict = dict(Message=message, ClientState=client_state, Type=response_type)
        return Response(response_dict, status=status.HTTP_200_OK)

    def record_session(self, data):
        session, created = UssdRecord.objects.update_or_create(session_id=self.session_id, phone_no=self.phone_no,
                                                               gateway=self.gateway,
                                                               defaults=data)
        return session

    def exit_session(self):
        return self.process_response(message='Thank You', client_state=FINISH, response_type=RELEASE)

    def get_ussd_record(self):
        try:
            return UssdRecord.objects.get(session_id=self.session_id)
        except Exception as e:
            return None
