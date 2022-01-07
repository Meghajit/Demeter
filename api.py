import datetime
from flask import Flask
from flask import request
from flask_cors import CORS,cross_origin
from MutualFund import MutualFund

app = Flask(__name__)
CORS(app, resources=r'/v1/*')

class Demeter:

    @app.route('/v1/fundhouses')
    def get_fund_houses():
        response = app.make_response(MutualFund.get_fund_houses())
        response.content_type = "application/json"
        return response

    @app.route('/v1/fundhouse/<int:fund_house_id>/schemes')
    def get_schemes(fund_house_id: int):
        response = app.make_response(MutualFund.get_fund_house_schemes(fund_house_id))
        response.content_type = "application/json"
        return response

    @app.route('/v1/nav', methods=["POST"])
    def get_historic_nav():
        
        req_body = request.json


        start_date_splitted = req_body["startDate"].split('-')
        start_date = datetime.datetime(int(start_date_splitted[0]), int(start_date_splitted[1]),
                                       int(start_date_splitted[2]))
        end_date_splitted = req_body["endDate"].split('-')
        end_date = datetime.datetime(int(end_date_splitted[0]), int(end_date_splitted[1]), int(end_date_splitted[2]))
        response = app.make_response(MutualFund.get_historic_nav(
            req_body["fundHouseId"], req_body["schemeId"], start_date, end_date))
        response.content_type = "application/json"
        return response