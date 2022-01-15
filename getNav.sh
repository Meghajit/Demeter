#!/bin/bash
###########################################################################################
#Purpose: Invoke historical NAV for a particular MF scheme everyday using a crontab job  #
#Name: getNav.sh                                                                          #
#Author: Pinak Mazumdar                                                                   #
###########################################################################################
getFundHouseID()

{
URL="localhost:8080/v1/fundhouses"
FUND_HOUSES=`curl --location --request GET "$URL"`
FUND_HOUSE_ID=`echo $FUND_HOUSES | jq  '.[] | select(.fund_house=="Mirae Asset Mutual Fund")' | jq '.fund_house_id'`
echo $FUND_HOUSE_ID
}

getSchemes()

{
 id=${FUND_HOUSE_ID}
 URL="localhost:8080/v1/fundhouse/${id}/schemes"
 SCHEMES=`curl --location --request GET "$URL"`
 SCHEME_ID=`echo $SCHEMES | jq  '.[] | select(.scheme_name=="Mirae Asset Tax Saver Fund-Direct Plan -Growth")' | jq '.scheme_id'`
 echo $SCHEME_ID
}


getNAV()
{

enddate=`date -d '1 day ago' +'%Y-%m-%d'`
startdate=`date -d '1 day ago' +'%Y-%m-%d'`
fundid="$FUND_HOUSE_ID"
schemeid="$SCHEME_ID"
CURLURL="localhost:8080/v1/nav"
CURLDATA="{\
"\"startDate"\": "\"${startdate}"\", \
"\"endDate"\": "\"${enddate}"\", \
"\"fundHouseId"\": "${fundid}", \
"\"schemeId"\": "${schemeid}"\
}"

RESPONSE=`curl --location --request POST "$CURLURL" --header 'Content-Type: application/json' --data-raw  "$CURLDATA"`
#echo "Latest NAV: ${RESPONSE}"
}

getParsedOutput(){
date=`echo $RESPONSE | jq '.[].date'`
nav=`echo $RESPONSE | jq '.[].nav'`
#echo $date
#echo $nav
msg="Dear \${PERSON_NAME} \n\nThank you for showing interest in receiving daily NAV details for your selected mutual fund scheme. \n\nThe NAV(Net Asset Value) for the mutual fund scheme you selected is ${nav} as on ${date}. \n\nIf you want to unsubscribe from this service.Please send SMS STOP NAV to 9742061425.\n\nThanks,\nAnna-konda"
echo -e "$msg" >files/getNAV.out
}


##Main function
startProcess()
{
FLASK_APP=api.py flask run --port=8080
}

startProcess &
sleep 5
getFundHouseID
getSchemes $FUND_HOUSE_ID
getNAV $FUND_HOUSE_ID $SCHEME_ID
getParsedOutput $RESPONSE
python3 send_email.py
echo "-----End of Script------"

