# Payment Gateway and Background Processing for Photo & Portrait Orders using Stripe, Celery, Redis, and FastAPI

This project handles a payment gateway and the processing of online portrait photos.

It receives customers' photos and caches them in Redis until payment is confirmed, at which point it processes the storage and owner notification in the background using Celery.

The idea behind this approach is to ensure that the photos are only stored after payment is confirmed and to process them in the background to avoid performance issues.

Below is a quick demonstration of how it works.
![](media/demo.gif)

The project uses:

- [Jinja templates](https://jinja.palletsprojects.com/en/stable/) for frontend and email templates
- [FastAPI](https://fastapi.tiangolo.com/) for the backend and template rendering endpoints
- [Stripe](https://stripe.com/pt-pt) to process the payment gateway
- [Celery](https://docs.celeryq.dev/en/stable/index.html) to process tasks in the background
- Redis to cache values and also serve as the Celery broker and backend
- PostgreSQL to store all the order information
- Google API to perform address validation
- [Fastapi-mail](https://sabuhish.github.io/fastapi-mail/) to send emails
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) to store photos in AWS S3
- [pytest](https://docs.pytest.org/en/stable/), [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/config.html), [testscontainers-python](https://testcontainers-python.readthedocs.io/en/latest/), and [pytest-mock](https://pytest-mock.readthedocs.io/en/latest/) to perform tests
- [Docker](https://www.docker.com/) to orchestrate all the services together

### How it works


![](media/workflow.png)

### How to run this project

### Notes

- The project focused in the backend payment flow, and the edge cases where not tread, and can be done as futher steps
- templates are in async routes just due to the test coverage
