from requests_html import HTMLSession
import json
import datetime


class MutualFund:

    def __init__(self):
        pass

    @staticmethod
    def get_fund_houses() -> json:
        try:
            session = HTMLSession()
            request_url = 'https://www.amfiindia.com/net-asset-value/nav-history'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
                'Accept': 'text/html'
            }
            html_response = session.request(method="GET", url=request_url, headers=headers)
            fund_house_option_tags = html_response.html.find('#NavHisMFName > option')
            del fund_house_option_tags[0]
            fund_houses = []
            for house in fund_house_option_tags:
                fund_houses.append(
                    {"fund_house": house.text,
                     "fund_house_id": int(house.attrs['value'])})
            return json.dumps(fund_houses)
        except Exception as inst:
            print(inst)
            result = {
                "success": False,
                "error-message": "Something went wrong. Could not fetch stocks data."
            }
            return json.dumps(result)

    @staticmethod
    def get_fund_house_schemes(fund_house_id: int) -> json:
        try:
            session = HTMLSession()
            request_url = 'https://www.amfiindia.com/modules/NavHistorySchemeNav'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            data = 'ID=' + str(fund_house_id)
            raw_scheme_list = session.request(method="POST", url=request_url, headers=headers, data=data).json()
            schemes = []
            for scheme in raw_scheme_list:
                schemes.append({
                    "scheme_id": int(scheme['Value']),
                    "scheme_name": scheme['Text'].strip()
                })
            return json.dumps(schemes)
        except Exception as inst:
            print(inst)
            result = {
                "success": False,
                "error-message": "Something went wrong. Could not fetch stocks data."
            }
            return json.dumps(result)

    @staticmethod
    def get_formatted_date(date: datetime) -> str:
        return str(date.day) + "-" + date.strftime("%b") + str(date.year)

    @staticmethod
    def get_historic_nav(fund_house_id: int, scheme_id: int, start_date: datetime, end_date: datetime) -> json:
        try:
            session = HTMLSession()
            request_url = 'https://www.amfiindia.com/modules/NavHistoryPeriod'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
                'Accept': 'text/html',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }

            formatted_start_date = MutualFund.get_formatted_date(start_date)
            formatted_end_date = MutualFund.get_formatted_date(end_date)
            request_body = "mfID=" + str(fund_house_id) + "&scID=" + str(scheme_id) + "&fDate=" + formatted_start_date \
                           + "&tDate=" + formatted_end_date
            html_response = session.request(method="POST", url=request_url, headers=headers, data=request_body)
            table_rows = html_response.html.find('#divExcelPeriod > table > tbody > tr')
            nav_rows = table_rows[5:]
            historic_nav_list = []
            for index, nav_row in enumerate(nav_rows):
                historic_nav_list.append({
                    "nav": nav_row.find('td')[0].text,
                    "date": nav_row.find('td')[3].text,
                })
            return json.dumps(historic_nav_list)
        except Exception as inst:
            print(inst)
            result = {
                "success": False,
                "error-message": "Something went wrong. Could not fetch stocks data."
            }
            return json.dumps(result)
