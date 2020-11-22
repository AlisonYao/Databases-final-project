insert into airline values ('China Eastern');
insert into airport values ('JFK', 'NYC');
insert into airport values ('PVG', 'Shanghai');
insert into customer values ('alison@gmail.com', 'Alison Yao', '123456', 'Taylor Building', 'Cornelia Street', 'L.A.', 'California', '1893974386', 'X12345678', '2025-01-01', 'China', '2000-08-21');
insert into customer values ('clark@gmail.com', 'Clark Kent', 'IAmSuperman', 'Krypton Building', 'Lois Lane', 'Metropolis', 'New York', '1896468253', 'S19380418', '2035-01-01', 'US', '1988-02-29');
insert into airplane values ('China Eastern', '10101', 366);
insert into airplane values ('China Eastern', '20202', 853);
insert into airline_staff values ('Janet', 'theGoodPlace', 'Janet', 'Robot', '1978-02-05', 'China Eastern');
insert into flight values ('China Eastern', '11111', 'JFK', '2020-04-13 11:32:23', 'PVG', '2020-04-14 05:38:43', '5400', 'upcoming', '10101');
insert into flight values ('China Eastern', '22222', 'PVG', '2020-11-09 10:21:56', 'JFK', '2020-04-14 02:25:31', '3400', 'delayed', '20202');
insert into ticket values ('12345', 'China Eastern', '11111');
insert into ticket values ('74373', 'China Eastern', '11111');
insert into ticket values ('63627', 'China Eastern', '22222');
insert into ticket values ('02758', 'China Eastern', '22222');
insert into ticket values ('10000', 'China Eastern', '22222');
insert into booking_agent values ('Dani@gmail.com', 'Jamie123', '98765');
insert into purchases values ('12345', 'alison@gmail.com', '98765', '2020-01-01 12:34:21');
insert into purchases values ('63627', 'clark@gmail.com', null, '2020-01-01 11:45:23');
