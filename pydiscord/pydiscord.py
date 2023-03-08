import time
import json
import requests


class Discord:
    def __init__(self):
        pass

    def generateFingerprint(self):
        url = "https://discord.com/api/v9/experiments?with_guild_experiments=true"

        payload = {}
        headers = {
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'X-Debug-Options': 'bugReporterEnabled',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'X-Discord-Locale': 'en-US',
            'sec-ch-ua-platform': '"Windows"',
            'Accept': '*/*',
            'host': 'discord.com',
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            return response.json()['fingerprint']

        return -1

    def solve_captcha(self):
        send_data = {
            "clientKey": 'CAI-1EB16E4FC4F672FE6E51B3E8DB70BFC8',
            "task": {
                "type": 'HCaptchaTaskProxyless',
                'websiteURL': 'https://discord.com/channels/@me',
                "websiteKey": '4c672d35-0701-42b2-88c3-78380b0db560',

            }
        }
        headers = {
            'Host': 'api.capsolver.com',
            'Content-Type': 'application/json'
        }
        response = requests.post('https://api.capsolver.com/createTask', headers=headers, json=send_data)

        return self.check_status(response.json()['taskId'])

    def check_status(self, task_id):
        headers = {
            'Host': 'api.capsolver.com',
            'Content-Type': 'application/json'
        }
        payload = {
            'clientKey': 'CAI-1EB16E4FC4F672FE6E51B3E8DB70BFC8',
            'taskId': task_id
        }
        solved = False
        while not solved:
            response = requests.post('https://api.capsolver.com/getTaskResult', headers=headers, json=payload).json()
            print(response)
            if response['status'] == 'ready':
                solution = response['solution']['gRecaptchaResponse']
                user_agent = response['solution']['userAgent']

                return solution, user_agent
            print('Checking captcha after 1.5 seconds')
            time.sleep(1.5)

    def register_discord(self):
        captcha, user_agent = self.solve_captcha()
        fingerprint = self.generateFingerprint()
        print(captcha, fingerprint, user_agent)
        url = "https://discord.com/api/v9/auth/register"

        payload = json.dumps({
          "fingerprint": fingerprint,
          "email": "meisipalmson19831@outlook.com",
          "username": "meisipalmson12981",
          "password": "57910000@Aymane@A",
          "invite": None,
          "consent": True,
          "date_of_birth": "1998-02-04",
          "gift_code_sku_id": None,
          "captcha_key": captcha,
          "promotional_email_opt_in": False
        })
        headers = {
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'X-Fingerprint': fingerprint,
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwOS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTA5LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyIsInJlZmVycmluZ19kb21haW4iOiJ3d3cuZ29vZ2xlLmNvbSIsInNlYXJjaF9lbmdpbmUiOiJnb29nbGUiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTc1MTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9',
            'X-Debug-Options': 'bugReporterEnabled',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'X-Discord-Locale': 'en-US',
            'sec-ch-ua-platform': '"Windows"',
            'Accept': '*/*',
            'host': 'discord.com',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
