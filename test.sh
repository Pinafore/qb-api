docker-compose -f docker-compose.dev.yml up -d
sleep 2
docker-compose -f docker-compose.test.yml up
docker-compose -f docker-compose.dev.yml down
