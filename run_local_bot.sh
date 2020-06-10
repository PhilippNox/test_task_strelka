#/bin/bash

if [[ $(uname) != "Darwin" ]];then
    echo "⚠️  This script work at macOS"
    exit
fi

run_n_term() {
  PTH=$(pwd)
  osascript -e "tell app \"Terminal\"
    do script \"cd $PTH && $1\"
  end tell"
}

TOKEN=$(cat .env | grep TG_TOKEN_MAIN | cut -d '=' -f2)
NG_PTH=$(cat .env | grep NGROK_PATH | cut -d '=' -f2)
DEF_USER=$(cat .env | grep DEF_USER | cut -d '=' -f2)
TG_WEBHOOK=$(cat .env | grep TG_WEBHOOK_MAIN | cut -d '=' -f2)

SPECIAL='export DYLD_FALLBACK_LIBRARY_PATH=$HOME/anaconda/lib/:$DYLD_FALLBACK_LIBRARY_PATH'

run_n_term "$SPECIAL; uvicorn app.main:app --reload"
run_n_term "$NG_PTH http 8000"


#NG_URL=$(curl -s http://127.0.0.1:4040/api/tunnels/command_line | jq -r '.public_url')
while [[ -z "$NG_URL" || $NG_URL == "null" ]]; do
  sleep 1
  echo "wait ngrok url"
  NG_URL=$(curl -s http://127.0.0.1:4040/api/tunnels/command_line | jq -r '.public_url')
done
echo $NG_URL

#Check webhook
#curl -X GET "https://api.telegram.org/bot$TOKEN/getWebhookInfo"

curl -sX POST "https://api.telegram.org/bot$TOKEN/setWebhook" -H 'Content-Type:application/json' -H 'cache-control: no-cache' -d "{\"url\": \"$NG_URL$TG_WEBHOOK\"}" | jq -r '.description'
curl -s "https://api.telegram.org/bot$TOKEN/getWebhookInfo" | jq -r '.result.url'

#Send msg to user with DEF_USER
curl -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" -H 'Content-Type:application/json' -H 'cache-control: no-cache' -d "{\"chat_id\": $DEF_USER, \"text\":\"I'm here 🦾\"}"
