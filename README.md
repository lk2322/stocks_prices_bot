# Stocks price bot
### Build

-----
```
docker build . -t stock-bot-img
docker run -v stock_db:/db --env DB_URL=/db/test.db --env TOKEN={your_token} --name stock_bot stock-bot-img
```
