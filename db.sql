create table Vuelo( 
    ID_vuelo serial primarial key, 
    codigo_IATA varchar(3) not null,
    aeropuerto varchar(35) not null,
    lugar_de_ida varchar(35) not null,
    lugar_de_llegada varchar(35) not null,
    ciudad varchar(30) not null,
    asientos integer(1) not null,
    fecha_de_ida timestamp not null,
    fecha_de_llegada timestamp not null, 
);