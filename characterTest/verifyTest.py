#!/usr/bin/env python
#coding=utf-8
#pip install aliyun-python-sdk-core

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest
import random

def getVerifyCode(phoneNumber:str):
    VERIFYCODE = ''
    for i in range(6):
        VERIFYCODE += str(random.randint(0, 9))

    # credentials =
    # use STS Token
    # credentials = StsTokenCredential('<your-access-key-id>', '<your-access-key-secret>', '<your-sts-token>')
    client = AcsClient(region_id='cn-hangzhou', credential=credentials)

    request = SendSmsRequest()
    request.set_accept_format('json')

    request.set_PhoneNumbers(phoneNumber)
    request.set_SignName("成都设尔易科技有限公司")
    request.set_TemplateCode("SMS_249800306")
    request.set_TemplateParam({"code":VERIFYCODE})

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))
    return VERIFYCODE

