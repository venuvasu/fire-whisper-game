# Load variables from .env if it exists
ifneq (,$(wildcard .env))
  include .env
  export
endif

# Default environment if not specified
FIREWHISPER_ENV ?= Dev

BUCKET = dnd-lambda-deployer-bucket
STACK = fire-whisper-lambda-backend-$(shell echo $(FIREWHISPER_ENV) | tr A-Z a-z)
REGION = us-east-1

build:
	rm -rf backend/requests.installed
	rm -rf backend/requests*
	rm -rf backend/urllib3*
	python3 -m pip install -r backend/requirements.txt -t backend/
	touch backend/requests.installed

package: build
	sam package \
	  --template-file template.yaml \
	  --output-template-file packaged.yaml \
	  --s3-bucket $(BUCKET) \
	  --region $(REGION)

deploy:
	sam deploy \
	  --template-file packaged.yaml \
	  --stack-name $(STACK) \
	  --capabilities CAPABILITY_IAM \
	  --region $(REGION) \
	  --parameter-overrides \
	    FireWhisperUserPool=$(FIREWHISPER_USER_POOL) \
	    FireWhisperUserPoolClient=$(FIREWHISPER_USER_POOL_CLIENT) \
		Environment=$(FIREWHISPER_ENV)

delete:
	aws cloudformation delete-stack \
	  --stack-name $(STACK) \
	  --region $(REGION)

status:
	aws cloudformation describe-stacks \
	  --stack-name $(STACK) \
	  --region $(REGION) \
	  --query "Stacks[0].StackStatus"
