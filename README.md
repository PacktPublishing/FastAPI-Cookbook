# FastAPI Cookbook

<a href="https://www.packtpub.com/en-us/product/fastapi-cookbook-9781805127857"><img src="https://content.packt.com/_/image/original/B21025/cover_image_large.jpg" alt="Book Name" height="256px" align="right"></a>

This is the code repository for [FastAPI Cookbook](https://www.packtpub.com/en-us/product/fastapi-cookbook-9781805127857), published by Packt.

**Develop high-performance APIs and web applications with Python**

## What is this book about?
This book helps you unlock the power of FastAPI to build high-performing web apps and APIs by taking you through the basics like routing and data validation through to advanced topics, such as custom middleware and WebSockets.

This book covers the following exciting features:
* Explore advanced FastAPI functionalities such as dependency injection, custom middleware, and WebSockets
* Discover various types of data storage for powerful app functionality with SQL and NoSQL
* Implement testing and debugging practices for clean, robust code
* Integrate authentication and authorization mechanisms to secure web apps
* Acquire skills to seamlessly migrate existing applications to FastAPI
* Write unit and integration tests, ensuring reliability and security for your apps
* Deploy your FastAPI apps to production environments for real-world use

If you feel this book is for you, get your [copy](https://www.amazon.com/FastAPI-Cookbook-Develop-high-performance-applications/dp/1805127853) today!

<a href="https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" 
alt="https://www.packtpub.com/" border="5" /></a>


## Instructions and Navigations
All of the code is organized into folders. For example, Chapter02.

The code will look like the following:
```
from locust import HttpUser, task


class ProtoappUser(HttpUser):
    host = "http://localhost:8000"

    @task
    def hello_world(self):
        self.client.get("/home")
```

**Following is what you need for this book:**
This book is for Python developers looking to enhance their skills to build scalable, high-performance web apps using FastAPI. Professionals seeking practical guidance to create APIs and web apps that can handle significant traffic and scale as needed will also find this book helpful by learning from both foundational insights and advanced techniques. The book is also designed for anyone familiar with RESTful APIs, HTTP protocols, and database systems, as well as developers looking to migrate existing applications to FastAPI or explore its advanced features.

With the following software and hardware list you can run all code files present in the book (Chapter 1-12).

### Software and Hardware List

| Chapter  | Software required                   | OS required                        |
| -------- | ------------------------------------| -----------------------------------|
| 1-12     | Python 3.9 or higher                | Windows, Mac OS X, and Linux (Any) |


### Related products
* Hands-On Microservices with Django [[Packt]](https://www.packtpub.com/en-in/product/hands-on-microservices-with-django-9781835468524) [[Amazon]](https://www.amazon.com/Hands-Microservices-Django-cloud-native-applications/dp/1835468527)

* Node.js for Beginners [[Packt]](https://www.packtpub.com/en-us/product/nodejs-for-beginners-9781803245171) [[Amazon]](https://www.amazon.com/Node-js-Beginners-comprehensive-full-featured-applications/dp/1803245174)

## Get to Know the Author
**Giunio De Luca** is a software engineer with over 10 years of experience in fields such as physics, sports, and administration. He graduated in industrial engineering from the University of Basilicata and holds a PhD in numerical simulations from Paris-Saclay University. His work spans developing advanced algorithms, creating sports analytics applications, and improving administrative processes. As an independent consultant, he collaborates with research labs, government agencies, and start-ups across Europe. He also supports coding education in schools and universities through workshops, lectures, and mentorship programs, inspiring the next generation of software engineers with his expertise and dedication.
