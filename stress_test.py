from locust import HttpUser, task, between
import random
import uuid

class APIUser(HttpUser):
    wait_time = between(1, 2)  # Adjusted wait time for quicker interactions
    shortened_urls = []  # Shared list to store shortened URLs

    # List of real-world websites
    websites = [
        "https://www.amazon.in",
        "https://www.flipkart.com",
        "https://www.ebay.com",
        "https://www.walmart.com",
        "https://www.bestbuy.com",
        "https://www.target.com",
        "https://www.myntra.com",
        "https://www.snapdeal.com",
        "https://www.etsy.com",
        "https://www.alibaba.com",
        "https://www.costco.com",
        "https://www.bigbasket.com",
        "https://www.grofers.com",
        "https://www.shopify.com",
        "https://www.apple.com"
    ]

    def on_start(self):
        # Step 1: Signup with a unique email
        self.user_email = f"user_{uuid.uuid4().hex}@test.com"
        self.password = "password123"
        signup_response = self.client.post("/accounts/signup/", json={
            "email": self.user_email,
            "name": "test_user",
            "password": self.password
        }, headers={"Content-Type": "application/json"})
        
        if signup_response.status_code == 201:
            print(f"Signup successful: {self.user_email}")
            self.login_user()  # Proceed to login
            self.add_multiple_products()  # Add 15 products after successful login
        else:
            print(f"Signup failed: {signup_response.status_code}, {signup_response.text}")
            self.auth_token = None

    def login_user(self):
        # Step 2: Login to retrieve the access token
        login_response = self.client.post("/accounts/login/", json={
            "email": self.user_email,
            "password": self.password
        }, headers={"Content-Type": "application/json"})
        
        if login_response.status_code == 200:
            self.auth_token = login_response.json().get("access")  # Extract Bearer token
            print(f"Login successful for {self.user_email}, token: {self.auth_token}")
        else:
            self.auth_token = None
            print(f"Login failed: {login_response.status_code}, {login_response.text}")

    def add_multiple_products(self):
        # Step 3: Add 15 products for the user
        if not self.auth_token:
            print("Skipping add_multiple_products: Missing auth_token")
            return
        
        for _ in range(15):  # Add 15 products
            product_url = f"{random.choice(self.websites)}/product-{random.randint(1000, 9999)}"
            product_name = f"Product-{random.randint(1, 1000)}"
            response = self.client.post("/linker/shorten/", json={
                "product_url": product_url,
                "product_name": product_name
            }, headers={
                "Authorization": f"Bearer {self.auth_token}",
                "Content-Type": "application/json"
            })
            if response.status_code == 201:
                short_url = response.json().get("short_url")
                if short_url:
                    self.shortened_urls.append(short_url)
                    print(f"Product added, short_url: {short_url}")
            else:
                print(f"Add Product Failed: {response.status_code}, {response.text}")

    @task(1)  # Lower priority for product addition during the test
    def add_product(self):
        self.add_multiple_products()  # Use the same logic for product addition

    @task(10)  # High priority for hitting redirects
    def hit_redirect(self):
        if not self.shortened_urls:
            print("No shortened URLs available for redirection")
            return
        short_url = random.choice(self.shortened_urls)
        short_url_path = short_url.split("/")[-1]
        response = self.client.get(f"/redirect/{short_url_path}")
        print(f"Redirect hit: {short_url}, status: {response.status_code}")
