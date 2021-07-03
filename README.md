# Demeter

Demeter is an API to get all fund houses, their mutual fund schemes and the historic NAVs.

## REST Endpoints

### 1. Get all fund houses hosted: `GET /v1/fundhouses`

Sample cURL request

```shell
curl --location --request GET 'localhost:8080/v1/fundhouses'
```

Sample response

```json
[
  {
    "fund_house": "ABN AMRO Mutual Fund",
    "fund_house_id": 39
  },
  {
    "fund_house": "Aditya Birla Sun Life Mutual Fund",
    "fund_house_id": 3
  },
  {
    "fund_house": "AEGON Mutual Fund",
    "fund_house_id": 50
  }
]
```

### 2. Get all mutual fund schemes offered by the fund house: `GET /v1/fundhouse/:fund_house_id/schemes`

Sample cURL request

```shell
curl --location --request GET 'localhost:8080/v1/fundhouse/39/schemes'
```

Sample response

```json
[
  {
    "scheme_id": 105581,
    "scheme_name": "ABN AMRO Fixed Term Plan - Series 5: Quarterly Plan A - Dividend on Maturity Option"
  },
  {
    "scheme_id": 105579,
    "scheme_name": "ABN AMRO Fixed Term Plan - Series 5: Quarterly Plan A - Monthly Dividend Option"
  },
  {
    "scheme_id": 105580,
    "scheme_name": "ABN AMRO Fixed Term Plan - Series 5: Quarterly Plan A-Growth Option"
  },
  {
    "scheme_id": 102952,
    "scheme_name": "ABN  AMRO Opportunities Fund-Dividend"
  }
]
```

### 3. Get historic NAV for a mutual fund scheme: `POST /v1/nav`

Sample cURL request

```shell
curl --location --request POST 'localhost:8080/v1/nav' --header 'Content-Type: application/json' --data-raw '{
    "startDate": "2021-04-25",
    "endDate": "2021-04-30",
    "fundHouseId": 21,
    "schemeId": 112938
}'
```

Sample response

```json
[
  {
    "nav": "24.7657",
    "date": "26-Apr-2021"
  },
  {
    "nav": "24.7836",
    "date": "27-Apr-2021"
  },
  {
    "nav": "24.7843",
    "date": "28-Apr-2021"
  },
  {
    "nav": "24.7782",
    "date": "29-Apr-2021"
  },
  {
    "nav": "24.7922",
    "date": "30-Apr-2021"
  }
]
```