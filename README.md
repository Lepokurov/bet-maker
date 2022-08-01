Для создания образа нужно выполнить следущие команды

```commandline
docker build -t bet-maker .
docker tag bet-maker:latest bet-maker:stable
```
Для создания ставки нужно получить токен через POST /login урлу и использовать его через Bearer в POST /bets
