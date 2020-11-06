-- Project2 Question4
-- 1
select flight_num
from flight
where status = 'upcoming';

-- 2
select flight_num
from flight
where status = 'delayed';

-- 3
select customer.name
from purchase, customer
where purchase.c_email = customer.email and booking_agent_id is not null and ba_email is not null;

-- 4
select airplane.id
from airline natural join airplane
where airline.name = 'China Eastern';





