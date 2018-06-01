# A Basic Product Recommendation System
This is a basic recommendation system for an e-commerce company like Amazon,Flipkart based on search queries on Google/E-Commerce website.

Method:

Sample dataset is divided into 3 layers: 
1. Main Category of products (Eg. Electronics)
2. Sub Category (Eg. Mobile in Electronics category)
3. The Product (Eg. iPhone)

The program analyzes the queries, and give points to each product by some steps and then finally picks up top 'n' products to be displayed.

Steps to rate the product:
1) Searches if any query is related to Main Category. If yes , increments points of each product in that Main Category. <br>
    (In step 1, it increments points of Sub Category which then will increment points of each product)<br>
2) Searches if any query is related to Sub Category. If yes , increments points of each product in that Sub Category. <br>
3) Searches if any query is directly related to a product. If yes, increments points of the product and also all the products present in same sub category as the query-related product. (Eg, query- iPhone : Means user is looking for phone, so increments all phones. Obviously it needs to be more specific, but this is basic recommendation system).
<br><br>    (In step 3 , it increments Sub Category which then will increment points of each product. NOTE: The product directly searched is incremented twice , hence has highest number of points).
    
All other functions are just helper functions.
