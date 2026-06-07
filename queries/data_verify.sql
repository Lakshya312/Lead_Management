select Product.ProductID, Product.ProductName, Product_Category.CategoryName, Product.Is_Active from Product
inner join Product_Category ON Product.CategoryID = Product_Category.CategoryID;

SELECT count(*) FROM Product;

select * from Region;

use LeadManagementDB;