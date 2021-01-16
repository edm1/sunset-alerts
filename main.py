#!/usr/bin/env python

import sys
import time
import smtplib
import pprint
from email.mime.text import MIMEText
from pysunsetwx import PySunsetWx

def main(data, context):

    #
    # Set arguments -----------------------------------------------------------
    #
    
    args = Args()

    # SunsetWx
    args.sunsetwx_username = "sunsetwx_username"
    args.sunsetwx_password = "sunsetwx_password"
    args.latitude = 52.395734
    args.longitude = 0.270596
    args.place_name = 'Ely'
    args.prediction_type = "sunset"
    # Twitter
    args.tweet_min_quality = 50
    # Gmail
    args.gmail_username = "gmail_username"
    args.gmail_password = "gmail_password"
    args.email_recipient = "email_recipient"
    args.archive_quality = 50

    #
    # Run task ----------------------------------------------------------------
    #
    
    # Get prediction
    pred = sunsetwx_query_api(
        args.sunsetwx_username,
        args.sunsetwx_password,
        args.latitude,
        args.longitude,
        args.prediction_type
    )

    # Email the prediction
    if all([args.gmail_username, args.gmail_password, args.email_recipient]):
        send_gmail(
            args.gmail_username,
            args.gmail_password,
            args.email_recipient,
            pred,
            args.place_name,
            args.archive_quality
        )

    # Twitter
    # TODO

    return 0

def sunsetwx_query_api(username, password, latitude, longitude, prediction_type):
    ''' Query the SunsetWX api to get sunrise or sunset qualities
    '''

    # Instantiate PyPexels object
    py_sunsetwx = PySunsetWx(username, password)

    # Get sunset/sunrise quality
    quality = py_sunsetwx.get_quality(latitude, longitude, prediction_type)

    return quality

def send_gmail(username, password, to, pred, location, archive_quality):
    ''' Send the prediction via gmail 
    '''

    # Extract required values from the prediction
    quality = pred['features'][0]['properties']['quality']
    quality_perc = pred['features'][0]['properties']['quality_percent']
    pred_type = pred['features'][0]['properties']['type']
    
    # Create text
    msg = MIMEText(pprint.pformat(pred, indent=4))
    if quality_perc < archive_quality:
        msg['Subject'] = f"SunsetWx {location} {pred_type} {quality} {quality_perc:.1f} [archive]"
    else:
        msg['Subject'] = f"SunsetWx {location} {pred_type} {quality} {quality_perc:.1f}"
    msg['From'] = username
    msg['To'] = to

    # Send email
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(username, password)
    server.sendmail(username, to, msg.as_string())
    server.close()
    print('Email sent!')

    return 0

class Args:
    pass

if __name__ == '__main__':

    main('data', 'context')
