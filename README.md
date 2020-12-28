Мікросервіс крутиться на окремому сервері на DO, розгорнутий з допомогою docker-compose(python+postgres+nginx+certbot), прикручений SSL сертифікат від Lets Encrypt. Зрештою - по коду все видно. 

Власне сам сервіс тут - https://piastrix.tk/

Проблема:
pay method INVOICE for RUB didn't work because for error from the server:
response = `{
  "data": null, 
  "error_code": 3, 
  "message": "Payway (alias = payeer_rub) is not available for shop", 
  "result": false
}`

