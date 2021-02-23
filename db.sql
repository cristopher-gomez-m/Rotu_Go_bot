    ID_vuelo serial primary key, 
	aeropuerto_origen varchar(35) not null,
    codigo_IATA_origen varchar(3) not null,
	aeropuerto_destino varchar(35) not null,
	codigo_IATA_destino varchar(3) not null,
	lugar_de_origen varchar(35) not null,
    lugar_de_llegada varchar(35) not null,
    asientos integer(1) not null,
    fecha_de_ida timestamp not null,
    fecha_de_llegada timestamp not null 
);