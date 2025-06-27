# Fire Whisper Web UI

## Running Locally

npm run dev

## To Deploy

npm run build
aws s3 sync dist/ s3://{BUCKETNAME}/ --delete

| Environment | S3 Bucket              |
| ----------- | ---------------------- |
| Development | rpg-test-domain-bucket |
| Staging     |                        |
| Production  |                        |
