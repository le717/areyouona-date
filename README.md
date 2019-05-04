# Are you on a Date?

> Determine if you are currently on a date!

## Install

1. Install Python 3.7+ and [Poetry](https://poetry.eustace.io/)
1. Rename `oss.env` to `.env`
1. Set missing environment variables
1. `poetry install`
1. `poetry shell`
1. `flask run`

## Build/Deploy

1. `docker build -f "Dockerfile" -t areyouona-date:latest .`
1. `docker run -d --name areyouona-date -p 5000:5000 -t areyouona-date:latest`

## License

2018-2019 Caleb Ely

[MIT](LICENSE)

Candle image from [http://www.clker.com/clipart-10651.html](http://www.clker.com/clipart-10651.html)
