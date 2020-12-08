-- let's define 4 triggers which update #tickets left automatically
-- DO NOT RUN TESTING TRIGGERS!!!

-- only the first two are acutally useful
drop trigger if exists add_tickets;
create trigger add_tickets before insert on ticket
for each row
	update flight
    set num_tickets_left = num_tickets_left + 1
    where flight.airline_name = NEW.airline_name and flight.flight_num = NEW.flight_num;


drop trigger if exists delete_tickets;
create trigger delete_tickets after insert on purchases
for each row 
	update flight natural join ticket natural join purchases
    set num_tickets_left = num_tickets_left - 1
    where NEW.ticket_id = ticket.ticket_id;

-- for testing purposes, in case you are modifying DB manually plz also use the following ones

-- if you delete from tickets # goes down
drop trigger if exists delete_tickets_DB;
create trigger delete_tickets_DB after delete on ticket
for each row
	update flight
    set num_tickets_left = num_tickets_left - 1
    where flight.airline_name = old.airline_name and flight.flight_num = old.flight_num;

-- DELETE FROM ticket where ticket_id = '74373';


-- if you delete from purchases, # should go up
drop trigger if exists add_tickets_DB;
create trigger add_tickets_DB before delete on purchases
for each row 
	update flight natural join ticket natural join purchases
    set num_tickets_left = num_tickets_left + 1
    where old.ticket_id = ticket.ticket_id;

-- DELETE FROM purchases where ticket_id = '12345';


-- check all your triggers
show triggers;




-- -- ------------------------------------------------------------------------------------------------
-- -- test of prepared procedures
-- -- ------------------------------------------------------------------------------------------------
-- DELIMITER //
-- create procedure
-- booking_agent_registration (in email_input varchar(50), in password_input varchar(50), in booking_agent_id_input int(11))
-- begin
-- 	insert into booking_agent(email, password, booking_agent_id)
--     values (email_input, password_input, booking_agent_id_input);
-- end //
-- DELIMITER ;

-- call booking_agent_registration('someEmail1@gmail.com', '12345645678987654er5678987654567890987654356789hcxcvhjklhgfdfxzdxcgvhjhkjhugfygdcvbnkjhgufhv', '123456');
-- -- insert into booking_agent values ('Dani2@gmail.com', 'Jamie123765432456dfghjklkjhgfdsjhgfdsafghjgfdghmjrwhdfgnggfnhgergnfgtregnfrtgegerfngtegrgregfreggfre', '98765');
-- delete from booking_agent;




-- -- ------------------------------------------------------------------------------------------------
-- -- test of prepared statement
-- -- ------------------------------------------------------------------------------------------------
-- PREPARE statement1 FROM 'select * from airplane where airplane_id = ?';
-- SET @id = 10101; 
-- set @id2 = 20202;
-- EXECUTE statement1 USING @id;
-- EXECUTE statement1 USING @id2;

-- prepare statement2 from 'select * from airline_staff where username = ?';
-- set @username = ' 2 or 1 = 1; -- ';
-- execute statement2 using @username;


-- select * from airline_staff where username = 2 or 1 = 1; -- ;





-- -- ------------------------------------------------------------------------------------------------
-- -- test of triggers
-- -- ------------------------------------------------------------------------------------------------

-- create trigger add_tickets after insert on ticket
-- for each row
-- 	update flight
--     set num_tickets_left = num_tickets_left + 1
--     where flight.airline_name = NEW.airline_name and flight.flight_num = NEW.flight_num;

-- insert into ticket values ('32545', 'China Eastern', '11111');
-- insert into ticket values ('33545', 'China Eastern', '22222');

-- insert into ticket values ('32585', 'China Eastern', '11111');
-- insert into ticket values ('33585', 'China Eastern', '22222');






-- insert into purchases values ('127758', 'clark@gmail.com', null, '2020-03-11 12:34:21'); -- not working





-- -- drop trigger if exists delete_tickets;
-- -- DELIMITER //
-- -- create trigger delete_tickets after insert on purchases
-- -- for each row 
-- -- BEGIN
-- -- 	IF NEW.ticket_id = ticket.ticket_id 
-- --     -- IF NEW.ticket_id > 0
-- --     THEN
-- -- 		UPDATE flight, ticket
-- -- 		SET num_tickets_left = num_tickets_left - 1
-- -- 		WHERE flight.airline_name = ticket.airline_name and flight.flight_num = ticket.flight_num;
-- --     END IF;
-- -- END;
-- -- //
-- -- insert into purchases values ('33585', 'clark@gmail.com', null, '2020-08-11 12:34:21'); 







   
-- -- drop trigger if exists delete_tickets_view
-- -- create trigger delete_tickets_view after insert on purchases
-- -- for each row 
-- -- 	update customer_spending
-- --     set num_tickets_left = num_tickets_left - 1
-- --     where NEW.ticket_id = customer_spending.ticket_id;

-- -- insert into purchases values ('33545', 'clark@gmail.com', null, '2020-06-11 12:34:21');


-- drop trigger if exists testing;
-- DELIMITER //
-- create trigger testing after insert on purchases
-- for each row 
-- begin
-- 	declare x, np int(11) default 0;
--     declare an string;
--     set x = New.ticket_id;
-- end;
-- //
-- DELIMITER ;

-- set @tid = 00000;
-- select @tid;

-- insert into purchases values ('400880', 'clark@gmail.com', null, '2020-10-11 12:34:21');
-- select @tid;





-- show triggers;
