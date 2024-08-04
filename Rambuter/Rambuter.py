
import os
import random
import time
import secrets

import faker
from faker import Faker

from playwright.sync_api import Playwright, sync_playwright, expect

from twocaptcha import TwoCaptcha

import requests
from requests.exceptions import ConnectionError


proxy = {"server": "5.8.13.50:9235",
         "username": "UBNMup",
         "password": "xrsXCU"}


class Autoreg_for_rambler:
    def __init__(self, playwright: Playwright, proxy: dict = {}, headless: bool = True, api_key_2captcha: str = ''):
        if proxy != {}:
            self.browser = playwright.chromium.launch(headless=headless,
                                                      proxy={
                                                          "server": f"http://{proxy['server']}",
                                                          "username": proxy['username'],
                                                          "password": proxy['password']
                                                      }
                                                      )
        else:
            self.browser = playwright.chromium.launch(headless=headless)

        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.api_key_2captcha = api_key_2captcha

    def get_hCaptcha_result(self, api_key: str):
        solver = TwoCaptcha(api_key)
        try:
            result = solver.hcaptcha(sitekey='322e5e22-3542-4638-b621-fa06db098460', url='https://mail.rambler.ru/', )
            print(result)
            return result['code']

        except Exception as e:
            print(e)

    def check_proxy(self, proxy):
        try:
            # �������� ������ � ������� GET-������� � google.com
            resp = requests.get('http://google.com', proxies={'http': proxy})
            return True
        except ConnectionError:
            return False

    def hCaptcha_reaponce(self, page, captcha_token: str):
        frame = page.wait_for_selector("iframe[title=\"������ � ������� ��� �������� ������������ hCaptcha\"]")

        print(frame)
        print("����� �������")

        page.evaluate(
            'args => console.log(args)',
            [frame, captcha_token],
        )
        time.sleep(120)
        page.evaluate(
            'args => args[0].setAttribute("data-hcaptcha-response", args[1])',
            [frame, captcha_token],
        )
        page.evaluate(
            'args => document.querySelector(args[0]).value = args[1]',
            ['textarea[name=h-captcha-response]', captcha_token],
        )
        page.evaluate('code => hcaptcha.submit(code)', captcha_token)
        page.wait_for_timeout(500)

    def generate_person(self):
        fake = Faker()
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        return {'first_name': first_name, 'last_name': last_name, 'email': email[0:email.find('@example')] + chr(random.randint(65,90))+ chr(random.randint(65,90))+ chr(random.randint(65,90))}

    def generate_password(self):
        # ��������� ���������� ������ ������ 12 ��������
        password = ''.join(
            secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@$%^&*()') for _ in
            range(12))
        return password

    def write_to_file(self, file_name, var1, var2):
        with open(file_name, "a") as file:
            file.write(f"{var1} {var2}\n")

    def steps(self, first_name, last_name, email, password):

        self.page.goto("https://mail.rambler.ru/")

        # ������������������ �������� �� �������� �����������
        self.page.frame_locator("#root iframe").get_by_role("link",
                                                            name="�����������").click()  # ������� ������ ��� ������ ���������� ����� ��� �����������

        time.sleep(5)

        self.page.frame_locator("#root iframe").get_by_placeholder(
            "�����").click()  # ������� �� ���� ���������� �����
        self.page.frame_locator("#root iframe").get_by_placeholder("�����").fill(
            email)  # ���������� ���� �����

        time.sleep(5)
        self.page.frame_locator("#root iframe").get_by_placeholder(
            "���������� ������").click()  # ������� �� ���� ���������� ������
        self.page.frame_locator("#root iframe").get_by_placeholder("���������� ������").fill(
            password)  # ���������� ���� ������

        time.sleep(5)
        self.page.frame_locator("#root iframe").get_by_placeholder(
            "������ ������").click()  # ������� �� ���� ���������� ������� ������
        self.page.frame_locator("#root iframe").get_by_placeholder("������ ������").fill(
            password)  # ���������� ���� ������� ������

        time.sleep(5)
        self.page.frame_locator("#root iframe").get_by_placeholder(
            "����� ��������").click()  # ������� �� ���� ���������� ������ ��������
        self.page.frame_locator("#root iframe").get_by_placeholder("����� ��������").fill(
            "9999999999")  # ���������� ���� ������ ��������

        time.sleep(5)
        self.page.frame_locator("#root iframe").get_by_role("button",
                                                            name="�������� ���").click()  # ������� ������ ��� ��������� ���� �� ����������

        time.sleep(5)

        # ���������� ������� �����
        # -----------------------------------------------------------------------------------------------------------------------
        self.hCaptcha_reaponce(page=self.page,
                               captcha_token=self.get_hCaptcha_result('8a5b456af6cbcb44009f4b9387433b7a'))
        # -----------------------------------------------------------------------------------------------------------------------
        # ����������� ������������������ �������� �� �������� �����������
        self.page.frame_locator("#root iframe").get_by_role("button",
                                                            name="�������� ���").click()  # ��������� ������� ������ ��� ��������� ���� �� ����������
        self.page.frame_locator("#root iframe").get_by_placeholder(
            "��� �������������").click()  # ������� �� ���� ���������� ����
        self.page.frame_locator("#root iframe").get_by_placeholder("��� �������������").fill(
            "99999")  # ���������� ���� ����
        # -----------------------------------------------------------------------------------------------------------------------
        self.page.frame_locator("#root iframe").get_by_role("button", name="�����").click()

        # ���������� ���������� ����� � ������� �� ����� ���������� ���. ����������
        self.page.frame_locator("#root iframe").get_by_placeholder("���").click()  #
        self.page.frame_locator("#root iframe").get_by_placeholder("���").fill(first_name)  # ���������� �����

        self.page.frame_locator("#root iframe").get_by_placeholder("�������").click()  #
        self.page.frame_locator("#root iframe").get_by_placeholder("�������").fill(last_name)  # ���������� �������

        # ���������� �����������
        self.page.frame_locator("#root iframe").get_by_role("button", name="��������� �����������").click()
        self.page.frame_locator("#root iframe").get_by_text("�������� �������").click()

        # ---------------------
        self.context.close()
        self.browser.close()

    def run(self):


        while True:
            if self.check_proxy(proxy['server']):
                try:
                    person = self.generate_person()
                    password = self.generate_password()
                    self.steps(first_name=person['first_name'], last_name=person['last_name'], email=person['email'],
                                 password=password)

                    self.__write_to_file('profiles', person["email"], password)
                except Exception as eror:
                    print('���-��, ����� �� ���!', eror)
            else:
                print(f"������ {proxy['server']} ������ �� ������������")
                break


if __name__ == '__main__':
    with sync_playwright() as playwright:
        Autoreg_for_rambler(playwright, proxy={}, headless=False, api_key_2captcha='8a5b456af6cbcb44009f4b9387433b7a').run()