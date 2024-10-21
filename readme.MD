Here's a **README template** for your Django project based on the requirements you mentioned. You can customize it further based on your actual implementations.

---

## **Fruitables Django Project**  

This project demonstrates rendering templates, views, and URLs in Django. It provides pages for displaying product listings, product details, shopping cart, checkout, and more, along with the corresponding models for categories, products, and cart items.

---

### **Project Structure**  
1. **Templates**:  
   HTML files have been customized and structured using a `base.html` template to ensure reusability. Repetitive parts (like headers, footers) are extracted into partials.  

   - **Home Page**: `/`  
   - **Category Listing**: `/category/<slug:slug>/`  
   - **Product Details**: `/product/<slug:slug>/`  
   - **Cart**: `/order/cart/`  
   - **Checkout**: `/order/checkout/`  
   - **Contact Page**: `/contact/`  

2. **Static Files**:  
   CSS, JS, and images from the provided template are placed under the `static/` directory.  

---

### **Models Overview**  
1. **Category Model**:  
   - Fields: `name`, `slug`, `description`  
   - Purpose: To categorize products.  

2. **Product Model**:  
   - Fields: `name`, `slug`, `price`, `description`, `category (ForeignKey)`, `image`  
   - Purpose: Store product-related information.  

3. **Cart Model**:  
   - Fields: `user (ForeignKey)`, `created_at`  
   - Purpose: Track active carts for users.  

4. **CartItem Model**:  
   - Fields: `cart (ForeignKey)`, `product (ForeignKey)`, `quantity`  
   - Purpose: Represent items in the cart.  

---

### **Views and URLs**  
- **Home View**: Displays the homepage with navigation to other pages.  
- **Category View**: Lists all products under a given category.  
- **Product Detail View**: Displays detailed information about a specific product.  
- **Cart View**: Shows items in the user’s cart.  
- **Checkout View**: Collects order information.  
- **Contact View**: Displays a form for user inquiries.  

Each view is linked through Django’s `urls.py` to ensure seamless navigation across pages.

---

### **Setup Instructions**  
1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/pakhuridze/django-ecommerce.git
   cd fruitables
   ```

2. **Install Dependencies**:  
   Make sure Django is installed. If not, install it via:  
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Database Migrations**:  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run the Server**:  
   ```bash
   python manage.py runserver
   ```

5. **Access the Site**:  
   Open your browser and visit `http://127.0.0.1:8000/`.

---

### **Admin Access for Authorization**  
Use Django's admin interface for managing content and users.  
- **Credentials**: `username:saitama`, `password:admin`
- **Admin URL**: `/admin/`  
- **Create a superuser**:  
   ```bash
   python manage.py createsuperuser
   ```

---



