CREATE VIEW staff_flight AS
SELECT airplane_id, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, status
FROM flight NATURAL JOIN airline_staff;

create view agent_viewMyFlight as
select booking_agent.email, purchases.booking_agent_id, purchases.customer_email, purchases.purchase_date, purchases.ticket_id, flight.airline_name, flight.flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id
from booking_agent natural right outer join purchases natural join ticket natural join flight;

create view public_search_flight as
select flight_num, airline_name, airplane_id, D.airport_city as departure_city, departure_airport, departure_time, A.airport_city as arrival_city, arrival_airport, arrival_time, price, status
from airport as D, flight, airport AS A
where D.airport_name = departure_airport and A.airport_name = arrival_airport;

create view agent_commission as 
select email, purchases.ticket_id, customer_email, purchase_date, price as ticket_price
from booking_agent natural join purchases natural join ticket natural join flight;