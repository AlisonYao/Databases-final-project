-- test of prepared procedures
DELIMITER //
create procedure
booking_agent_registration (in email_input varchar(50), in password_input varchar(50), in booking_agent_id_input int(11))
begin
	insert into booking_agent(email, password, booking_agent_id)
    values (email_input, password_input, booking_agent_id_input);
end //
DELIMITER ;

call booking_agent_registration('someEmail1@gmail.com', '12345645678987654er5678987654567890987654356789hcxcvhjklhgfdfxzdxcgvhjhkjhugfygdcvbnkjhgufhv', '123456');
-- insert into booking_agent values ('Dani2@gmail.com', 'Jamie123765432456dfghjklkjhgfdsjhgfdsafghjgfdghmjrwhdfgnggfnhgergnfgtregnfrtgegerfngtegrgregfreggfre', '98765');
delete from booking_agent;





-- test of prepared statement
PREPARE statement1 FROM 'select * from airplane where airplane_id = ?';
SET @id = 10101; 
set @id2 = 20202;
EXECUTE statement1 USING @id;
EXECUTE statement1 USING @id2;

prepare statement2 from 'select * from airline_staff where username = ?';
set @username = ' 2 or 1 = 1; -- ';
execute statement2 using @username;


select * from airline_staff where username = 2 or 1 = 1; -- ;






