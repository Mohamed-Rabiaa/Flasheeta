#!/bin/bash
docker-compose exec flasheeta flask db init  
docker-compose exec flasheeta flask db migrate
docker-compose exec flasheeta flask db upgrade
