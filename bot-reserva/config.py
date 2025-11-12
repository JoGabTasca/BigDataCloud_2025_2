#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    # API Configuration
    API_BASE_URL = os.environ.get("API_BASE_URL", "https://chatbot-api-jgk-grbhazazdygrfsec.canadacentral-01.azurewebsites.net")
    CLU_ENDPOINT = "https://botluis-hotelreservation.cognitiveservices.azure.com"
    CLU_KEY = "6B8HAde3WPISgrsXoFxD1CDH58WOA46khHKrGNk2VZx3TdmwOpJKJQQJ99BKACBsN54XJ3w3AAAaACOG9H9C"
    CLU_PROJECT = "BotLuis-HotelReservation"
    CLU_DEPLOYMENT_NAME = "1o-mini"

