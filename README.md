# Are You On A Date?

> Determine if you are currently on a date!

## Install

1. Install Python 3.6+
1. Rename `oss.env` to `.env`
1. Set missing environment variables
1. `pip install pipenv`
1. `pipenv install`
1. `pipenv shell`
1. `flask run`

## Build/Deploy

1. `docker build -f "Dockerfile" -t areyouona-date:latest .`
1. `docker run -d --name areyouona-date -p 5000:5000 -t areyouona-date:latest`

## License

2018-2019 Caleb Ely

[MIT](LICENSE)

Candle image from [http://www.clker.com/clipart-10651.html](http://www.clker.com/clipart-10651.html)
