from flask import Flask, request, jsonify
from datetime import datetime
import hmac
import hashlib
import boto3
import uuid
from boto3.dynamodb.conditions import Attr
app = Flask(__name__)

class Authenticate:
    # init function will help initialize the credit card infomration 
    def __inti__(self,cardholderName,cardNumber,expiryDate,cvv,amount):
        self.cardholderName = cardholderName
        self.cardNumber = cardNumber
        self.expiryDate = expiryDate
        self.cvv = cvv
        self.amount = amount

    # this function will check if the amount enterted is within the credit limit
    def verifyCreditLimit(self):
        creditLimit = 20000 # 20,000 is the credit card limit
        if int(self.amount) > creditLimit:
            return False
        else:
            return True

    # this function will verify credit card format as per luhn algorithm 
    def verifyCreditCardFormat(self):
        #https://dev.to/seraph776/validate-credit-card-numbers-using-python-37j9
        
        if not self.cardNumber.isdigit():
            return False
        # Change datatype to list[int]
        cardNumberAsList = []
        for characterDigit in self.cardNumber:
            cardNumberAsList.append(int(characterDigit))

        #Remove the last digit:
        checkDigit = cardNumberAsList.pop()

        #Reverse the remaining digits:
        cardNumberAsList.reverse()
        
        for index,digit in enumerate(cardNumberAsList):
            if index % 2 ==0:
                cardNumberAsList[index] = digit*2

        #Subtract 9 at even indices if digit is over 9
        # (or you can add the digits)
      
        for index,digit in enumerate(cardNumberAsList):
            if index % 2 ==0 and digit > 9:
                cardNumberAsList[index] = digit - 9

        # Add the checkDigit back to the list:
        cardNumberAsList.append(checkDigit)

        # Sum all digits:
        checkSum = sum(cardNumberAsList)

        # If checkSum is divisible by 10, it is valid.
        if checkSum % 10 == 0:
            return True
        else:
            return False

    # this function will check the cvv which is supposed to be only digits of length 3 or 4
    def verifyCvv(self):
        if not self.cvv.isdigit():
            return False
        if len(self.cvv) not in [3,4]:
            return False
        return True

    # this function will verify the expriryy date which should always be greater than the current date
    def verifyExpiryDate(self):
        #datetime.strptime function will convert string datetime to datetime object
        expiryDateTimeobj = datetime.strptime(self.expiryDate, '%Y-%m-%d')

        dateNow = datetime.now()

        if expiryDateTimeobj > dateNow:
            return True
        else:
            return False
    
    def generateAuthenticationCode(self):
        #https://www.thesecuritybuddy.com/cryptography-and-python/how-to-use-hmac-in-python/#:~:text=We%20can%20use%20the%20hmac%20and%20the%20hashlib,%22Secret%20Message%22%20h%20%3D%20hmac.new%28key.encode%28%29%2C%20message.encode%28%29%2C%20hashlib.sha512%29.hexdigest%28%29%20print%28h%29
        secretKey = 'UgqpZ7pAWFqx4rBk8j5qL6mW34Jv9SvY' # secret key which was randomly used for the purpose the project
        cardInfo = self.cardholderName + self.cardNumber + self.expiryDate + self.cvv + self.amount
        # hash based message authentication code is generated using hmac.new method using secret key and card detail data
        authCode = hmac.new(secretKey.encode(), cardInfo.encode(), hashlib.sha256).hexdigest()
        return authCode

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb',region_name='us-west-2')

# Get the table
table = dynamodb.Table('PaymentTransactions')
    
def write_to_dynamodb(data):
    try:
        #to write the item into the table
        table.put_item(
            Item={
                "transaction_id": data['transaction_id'],
                "cardholder_name": data['cardholder_name'],
                "card_number": data['card_number'],
                "expiry_date": data['expiry_date'],
                "cvv": data['cvv'],
                "amount": data['amount'],
                "authentication_code": data['authentication_code']
            }
        )
        print("Insertion successfull")
        return True
    except Exception as e:
        #Handle exception
        print("Error writing to DynamoDB:", e)
        return False
    
def getTotalSpend(card_number):
    expression_attribute_values = {':cn': card_number}
    # Define filter expression 
    filter_expression = Attr('card_number').eq(card_number)
    # returns response after filtering the item that that matches the credit card number 
    response = table.scan(FilterExpression=filter_expression,ProjectionExpression='amount')
    # data will contain the list of items 
    data = response['Items']
    total_amount = 0
    # calculating the amount from the items resturned by the filter 
    for item in data:
        total_amount += int(item['amount'])  # converting amount  stored as string to an integer
    return total_amount

@app.route('/', methods=['POST'])
def receive():
    # get request is to make the query request to dynamodb to filter all the items with that specific card number send in the request body
    if request.method == 'GET':
        #geting the card_number spent 
        data = request.args.get('card_number')
        #calling the getTotalSpend to calculate the total spend on that credit card number
        total_amount = getTotalSpend(data)
        # the jsonfiy will convert dictionary object to json before returning the response 
        return jsonify({'success': True, 'total_amount': total_amount}), 200
    elif request.method == 'POST':
        data = request.form.to_dict() # the request body received as json is converted to dictionary 
        # checkAuthenticate is the object calling the class Authenticate which sends the card details for initialization
        checkAuthenticate = Authenticate(data['cardholder_name'],data['card_number'],data['expiry_date'],data['cvv'],data['amount'])

        # check will store the boolean value True or False based on the checks performed 
        check = checkAuthenticate.verifyCreditLimit() and checkAuthenticate.verifyCreditCardFormat() and checkAuthenticate.verifyCvv() and checkAuthenti>
    
        
        if check:
            #generating the unique Authentication code 
            uniqueAuthcode = checkAuthenticate.generateAuthenticationCode()
            # on successful authentiaction a dictionary object is created with message and authenticatiom code is generated
            response_data = {
            'message': 'Your Payment was Successful',
            'authenticationCode': uniqueAuthcode
            }
            
            # forming the credit card dictionary data to be able to send it to the write_to_dynamodb function 
            datatest = { "transaction_id": str(uuid.uuid4()), #generating unique transaction ID
                         "cardholder_name": request.form['cardholder_name'],
                         "card_number": request.form['card_number'],
                         "expiry_date": request.form['expiry_date'],
                         "cvv": request.form['cvv'],
                         "amount": request.form['amount'],
                         "authentication_code": uniqueAuthcode }
            #calling the dynamodb and checking the response
            if write_to_dynamodb(datatest):
                # the jsonfiy will convert dictionary object to json before returning the response 
                
                return jsonify(response_data), 200
            else:
                response_data = {
                'error': 'Insertion failed',
                }
                return jsonify(response_data), 401
        else:
            # on failure tof authentication a dictionary object is created with message to convey failure 
            response_data = {
            'error': 'Authentication failed',
            }
            # the jsonfiy will convert dictionary object to json before returning the response
            return jsonify(response_data), 401


if __name__ == '__main__':
    # when host is set to 0.0.0.0 which means the Fask application is accessbile from all IP address
    # The port 80 is the port number on which Flask application will be listening for incomming requests
    app.run(host='0.0.0.0', port=80)  
