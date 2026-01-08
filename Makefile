include .env

.PHONY: test-unit deploy-localstack deploy-test-env destroy-test-env generate-tfvars-file

LOCALSTACK_NAME := localstack

test-unit:
	uv run pytest src/tests/unit_tests

test-integration:
	uv run --env-file=.env pytest src/tests/integration_tests

deploy-localstack:
	docker ps --format '{{.Names}}' | grep -q $(LOCALSTACK_NAME) || docker run -d --rm \
		--name $(LOCALSTACK_NAME) \
		-p 4566:4566 \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-e SERVICES=lambda,iam,logs \
		localstack/localstack


deploy-test-env: deploy-localstack
	cd terraform && terraform init && terraform apply --auto-approve --var="aws_region=$(AWS_REGION)" --var="aws_lambda_name=$(AWS_LAMBDA_NAME)"

destroy-test-env:
	-cd terraform && terraform destroy --auto-approve
	-docker rm -f $(LOCALSTACK_NAME)
