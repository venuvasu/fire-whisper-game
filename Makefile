BUCKET = dnd-lambda-deployer-bucket
STACK = tavern-tales-lambda-backend
REGION = us-east-1

# Load variables from .env if it exists
ifneq (,$(wildcard .env))
  include .env
  export
endif

package:
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
	    TavernUserPool=$(TAVERN_USER_POOL) \
	    TavernUserPoolClient=$(TAVERN_USER_POOL_CLIENT)

delete:
	aws cloudformation delete-stack \
	  --stack-name $(STACK) \
	  --region $(REGION)

status:
	aws cloudformation describe-stacks \
	  --stack-name $(STACK) \
	  --region $(REGION) \
	  --query "Stacks[0].StackStatus"
