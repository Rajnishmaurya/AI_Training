--Section C - PostgreSQL / SQL
--Create a database named spare_parts_assessment. Connect to it and run spare_parts_setup.sql.
--Complete the following SQL tasks.
--C1. Display all parts belonging to the Mechanical category.

SELECT * from parts
where category='Mechanical'

--C2. Display parts with unit_price above 1000, ordered from highest price to lowest.

select * from parts
where unit_price>1000
order by unit_price DESC


--C3. Find the average unit_price for each category.
select category,avg(unit_price) as average_price from parts
group by category

--C4. Find the total stock quantity for each category.
select category,sum(stock_qty) as total_stock from parts
group by category

--C5. Display every purchase order with supplier_name, order_date and status using a JOIN.
select po.*, s.supplier_name from purchase_orders po
join suppliers s
	ON po.supplier_id=s.supplier_id

--C6. Join purchase_orders, purchase_order_items and parts to display po_id, part_name, quantity and
--unit_price.
select
	po.po_id,
	p.part_name,
	poi.quantity,
	p.unit_price
from purchase_orders po
join purchase_order_items poi
ON po.po_id=poi.po_id
JOIN parts p
on poi.part_id=p.part_id

--C7. Extend the previous query to calculate line_total = quantity × unit_price.
select
	po.po_id,
	p.part_name,
	poi.quantity,
	p.unit_price,
	(poi.quantity*p.unit_price) as line_total
from purchase_orders po
join purchase_order_items poi
ON po.po_id=poi.po_id
JOIN parts p
on poi.part_id=p.part_id

--C8. Use a LEFT JOIN to display all suppliers, including suppliers that have never received a purchase order.
select s.*,
	po.po_id,
	po.order_date,
	po.status
from suppliers s
left join purchase_orders po
on s.supplier_id=po.supplier_id

--C9. Display only suppliers that have no purchase orders.
select s.* from suppliers s
left join purchase_orders po
on s.supplier_id=po.supplier_id
where po.po_id is NULL

--C10. Create a view named purchase_order_summary showing po_id, supplier_name, part_name, quantity,
--unit_price, line_total and status. Query the view for Pending orders.
create or replace view purchase_order_summary as
select po.po_id,
	s.supplier_name,
	p.part_name,
	poi.quantity,
	p.unit_price,
	(poi.quantity*p.unit_price) as line_total,
	po.status
from purchase_orders po
join suppliers s
on po.supplier_id=s.supplier_id
join purchase_order_items poi
on po.po_id=poi.po_id
join parts p
on poi.part_id=p.part_id

select * from purchase_order_summary
where status='Pending'

--C11. Create a function calculate_part_discount(amount): if amount >= 2000 return 10% of amount, otherwise
--return 0. Use it with the parts table.
create or replace function calculate_part_discount(amount NUMERIC)
returns numeric language plpgsql as $$
BEGIN
	if amount>=2000 then
		return amount*0.10;
	else
		return 0;
	end if;
end;
$$;

select part_name,unit_price,calculate_part_discount(unit_price) as discount from parts


--C12. Create a function final_part_price(amount) that returns amount minus calculate_part_discount(amount).
--Use it in a SELECT query.
create or replace function final_part_price(amount NUMERIC)
returns numeric language plpgsql as $$
BEGIN
	return amount-calculate_part_discount(amount);
end;
$$;

select part_name,unit_price,final_part_price(unit_price) as final_price from parts

--C13. Create a stored procedure with parameters named update_po_status that accepts po_id and new_status
--and updates the matching purchase order. Call it once and verify the result.

create or replace procedure update_po_status(p_po_id INT,new_status VARCHAR)
language plpgsql as $$
begin
	update purchase_orders set status=new_status where po_id=p_po_id;
end;
$$;
call update_po_status(1,'Received');
select * from purchase_orders where po_id=1;


--C14. Create a stored procedure without parameters named mark_old_pending_orders that changes Pending
--orders dated before 2026-10-04 to Received. Run it and verify the results.
create or replace procedure mark_old_pending_orders()
language plpgsql as $$
begin
	update purchase_orders
	set status='Received'
	where status='Pending' and order_date<DATE '2026-10-04';
end;
$$;

call mark_old_pending_orders();

select * from purchase_orders where status='Received';

--C15. Normalization question: Suppose supplier_name, supplier_city, part_name, part_category, po_id and
--quantity were all stored repeatedly in one large table. Identify at least two repeated facts and suggest how you
--would separate the data into tables.
Normalize into separate tables:

suppliers(supplier_id,supplier_name,supplier_city)
parts(part_id,part_name,part_category)
purchase_orders(po_id,supplier_id,order_date,status)
purchase_order_items(po_id,part_id,quantity)

Repeated facts:
1. Supplier name and city repeat for every order from that supplier.
2. Part name and category repeat for every order containing that part.

Store supplier information once in suppliers and part information once in parts: foreign keys in purchase_orders and purchase_order_items.