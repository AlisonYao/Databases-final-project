CREATE VIEW staff_flight AS
SELECT airplane_id, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, status
FROM flight NATURAL JOIN airline_staff;

create view agent_viewMyFlight as
select booking_agent.email, purchases.booking_agent_id, purchases.customer_email, purchases.purchase_date, purchases.ticket_id, flight.airline_name, flight.flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id
from booking_agent natural right outer join purchases natural join ticket natural join flight;