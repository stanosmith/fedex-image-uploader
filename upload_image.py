import base64
import os
import requests


URL = os.environ.get("FEDEX_ENDPOINT", "https://ws.fedex.com:443/web-services")
KEY = os.environ.get("FEDEX_KEY")
PASSWORD = os.environ.get("FEDEX_PWD")
ACCOUNT_NUMBER = os.environ.get("FEDEX_ACCT_NUM")
METER_NUMBER = os.environ.get("FEDEX_METER_NUM")
HEADERS = {'Content-Type': 'text/xml'}


ENVELOPE = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v11="http://fedex.com/ws/uploaddocument/v11">
   <soapenv:Header/>
   <soapenv:Body>
      <v11:UploadImagesRequest>
         <v11:WebAuthenticationDetail>
            <v11:ParentCredential>
               <v11:Key>XXX</v11:Key>
               <v11:Password>XXX</v11:Password>
            </v11:ParentCredential>
            <v11:UserCredential>
               <v11:Key>{key}</v11:Key>
               <v11:Password>{password}</v11:Password>
            </v11:UserCredential>
         </v11:WebAuthenticationDetail>
         <v11:ClientDetail>
            <v11:AccountNumber>{account_number}</v11:AccountNumber>
            <v11:MeterNumber>{meter_number}</v11:MeterNumber>
         </v11:ClientDetail>
         <v11:TransactionDetail>
            <v11:CustomerTransactionId>UploadImagesRequest_v11</v11:CustomerTransactionId>
         </v11:TransactionDetail>
         <v11:Version>
            <v11:ServiceId>cdus</v11:ServiceId>
            <v11:Major>11</v11:Major>
            <v11:Intermediate>0</v11:Intermediate>
            <v11:Minor>0</v11:Minor>
         </v11:Version>
         <v11:Images>
            <v11:Id>{image_id}</v11:Id>
            <v11:Image>{base64_image}</v11:Image>
         </v11:Images>
      </v11:UploadImagesRequest>
   </soapenv:Body>
</soapenv:Envelope>
"""


def main(image_file, image_id):
    # open file and encode to b64
    with open(image_file, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read())

    # String substitution
    envelope = ENVELOPE.format(
        key=KEY,
        password=PASSWORD,
        account_number=ACCOUNT_NUMBER,
        meter_number=METER_NUMBER,
        image_id=image_id,
        base64_image=base64_image.decode("ascii")
    )

    # Send request
    response = requests.post(URL, data=envelope, headers=HEADERS)
    print(response.content)
    return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="FedEx Image Upload")
    parser.add_argument("-img", dest="filename", required=True, help="image file to be uploaded")
    parser.add_argument("-id", dest="imageid", required=True, help="Image Id enum value")

    args = parser.parse_args()
    main(args.filename, args.imageid)

