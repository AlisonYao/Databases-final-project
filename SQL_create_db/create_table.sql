create table airline(
	name varchar(20),
    primary key(name)
);

create table airline_staff(
	username varchar(20),
    password varchar(20),
    first_name varchar(20),
    last_name varchar(20),
    date_of_birth date,
    name varchar(20),
    foreign key(name) references airline(name) on delete CASCADE
);

create table airplane(
	name varchar(20),
    id char(5),
    seats smallint,
    primary key(name, id),
    foreign key(name) references airline(name) on delete CASCADE
);

create table airport(
	name varchar(20),
    city varchar(20),
    primary key (name)
);

create index airplaneID_index on airplane(id);
create table flight(
	name varchar(20),
    flight_num char(5),
    id char(5),
    departure_time datetime,
    departure_airport varchar(20),
    arrival_time datetime,
    arrival_airport varchar(20),
    price smallint,
    status varchar(20),
    primary key(name, flight_num),
    foreign key(id) references airplane(id) on delete CASCADE,
    foreign key(departure_airport) references airport(name) on delete CASCADE,
    foreign key(arrival_airport) references airport(name) on delete CASCADE
);

create table customer(
	email varchar(320),
    name varchar(20),
    password varchar(20),
    building_name varchar(20),
    street varchar(20),
    city varchar(20),
    state varchar(20),
    phone_number char(11),
    passport_number char(9),
    passport_expiration date,
    passport_country varchar(20),
    date_of_birth date,
    primary key(email)
);

create table booking_agent(
	email varchar(255),
    password varchar(20),
    booking_agent_id char(5),
    primary key(email)
);

create table ticket(
	ticket_id char(5),
    name varchar(20),
    flight_num char(5),
    primary key(ticket_id),
    foreign key(name, flight_num) references flight(name, flight_num) on delete CASCADE
);

create index bookingAgentID_index on booking_agent(booking_agent_id);
create table purchase(
	ticket_id char(5),
    c_email varchar(320),
    ba_email varchar(320),
    date datetime,
    booking_agent_id char(5),
    primary key(ticket_id, c_email),
    foreign key(ticket_id) references ticket(ticket_id) on delete CASCADE,
    foreign key(c_email) references customer(email) on delete CASCADE,
    foreign key(ba_email) references booking_agent(email) on delete CASCADE,
    foreign key(booking_agent_id) references booking_agent(booking_agent_id) on delete CASCADE
);







