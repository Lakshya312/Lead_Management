select Product.ProductID, Product.ProductName, Product_Category.CategoryName, Product.Is_Active from Product
inner join Product_Category ON Product.CategoryID = Product_Category.CategoryID;

SELECT count(*) FROM Lead;

select * from Product;
select * from Lead;
select * from Region;
select * from Territory;

SELECT *
FROM Territory
WHERE RegionID = 1;

use LeadManagementDB;