#!/usr/bin/env python

import sys
import time
import smtplib
import pprint
from email.mime.text import MIMEText
from pysunsetwx import PySunsetWx

def main(data, context):

    #
    # Configure app -----------------------------------------------------------
    #

    default_params = {
        "sunsetwx_username": "sunsetwx_username",
        "sunsetwx_password": "sunsetwx_password",
        "gmail_username": "gmail_username",
        "gmail_password": "gmail_password",
    }

    configs = {
        'Ely sunset': {
            # Sunsetwx
            "latitude": 52.395734,
            "longitude": 0.270596,
            "place_name": 'Ely',
            "prediction_type": "sunset",
            # Gmail
            "send_email": True,
            "email_recipients": ["email_recipient"],
            "email_min_quality": 0,
            "email_tags": [
                ('archive', lambda x: x < 50)
            ],
            # Twitter
            "send_tweet": False,
            "tweet_min_quality": 50
        },
        'Ely sunrise': {
            # Sunsetwx
            "latitude": 52.395734,
            "longitude": 0.270596,
            "place_name": 'Ely',
            "prediction_type": "sunrise",
            # Gmail
            "send_email": True,
            "email_recipients": ["email_recipient"],
            "email_min_quality": 0,
            "email_tags": [
                ('archive', lambda x: x < 50)
            ],
            # Twitter
            "send_tweet": False,
            "tweet_min_quality": 50
        },
    }

    #
    # Run each config ---------------------------------------------------------
    #

    for _, config in configs.items():

        # Add default params to config
        for key, val in default_params.items():
            if key not in config:
                config[key] = val

        # Get prediction
        pred = sunsetwx_query_api(
            config["sunsetwx_username"],
            config["sunsetwx_password"],
            config["latitude"],
            config["longitude"],
            config["prediction_type"]
        )
        quality_perc = pred['features'][0]['properties']['quality_percent']

        # Email the prediction
        if config['send_email'] and (quality_perc >= config['email_min_quality']):
            send_gmail(
                config["gmail_username"],
                config["gmail_password"],
                config["email_recipients"],
                pred,
                config["place_name"],
                config["email_tags"]
            )

        # Twitter
        # TODO

        time.sleep(5)

    return 0

def sunsetwx_query_api(username, password, latitude, longitude, prediction_type):
    ''' Query the SunsetWX api to get sunrise or sunset qualities
    '''

    # Instantiate PyPexels object
    py_sunsetwx = PySunsetWx(username, password)

    # Get sunset/sunrise quality
    quality = py_sunsetwx.get_quality(latitude, longitude, prediction_type)

    return quality

def send_gmail(username, password, to, pred, place_name, tag_rules):
    ''' Send the prediction via gmail 
    '''

    # Extract required values from the prediction
    quality = pred['features'][0]['properties']['quality']
    quality_perc = pred['features'][0]['properties']['quality_percent']
    pred_type = pred['features'][0]['properties']['type']

    # Get tags
    tags = [tag for (tag, cond) in tag_rules if cond(quality_perc)]
    if len(tags) > 0:
        tag_str = f' tags: {",".join(tags)}'
    else:
        tag_str = ''
    
    # Create text
    msg = MIMEText(pprint.pformat(pred, indent=4))
    msg['Subject'] = f"SunsetWx prediction {place_name} {pred_type} {quality} {quality_perc:.1f}{tag_str}"
    msg['From'] = username
    msg['To'] = ', '.join(to)

    # Send email
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(username, password)
    server.sendmail(username, to, msg.as_string())
    server.close()
    print('Email sent!')

    return 0

if __name__ == '__main__':

    main('data', 'context')
