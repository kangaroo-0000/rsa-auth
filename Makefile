#Makefile

IMAGE = fastimage
CONTAINER = fastcontainer
REPO_NAME = kangaroo-0000/rsa-auth

all: build run

build: 
	@docker build -t $(IMAGE) .

run: build
	@docker run -d --name $(CONTAINER) -p 8080:8080 $(IMAGE)
	echo "Build run. Visit http://127.0.0.1:8080/redoc"
push: 
	@docker push $(REPO_NAME)

clean:
	@docker stop $(CONTAINER)
	@docker rm $(CONTAINER)


