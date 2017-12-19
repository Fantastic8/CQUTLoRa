/*Change database*/
use CQUTLoRa;

/*Create LoRa User table*/
create table if not exists LUser(
	UserName varchar(20) binary not null,
	Passwd varchar(50) binary not null,
	Administrator boolean not null,
	primary key (UserName)
);

/*Create LoRa Node table*/
create table if not exists LNode(
	LoRaId varchar(10) binary not null,
	LoRaPD varchar(20) binary not null,
	LoRaStatus varchar(20) binary not null,
	primary key (LoRaId)
);

/*Create LoRa Gateway table*/
create table if not exists LGateway(
	LoRaId varchar(10) binary not null,
	LoRaPP char(10) binary not null,
	primary key (LoRaId)
);

/*Create LoRa Request User table*/
create table if not exists LRUser(
	UserName varchar(20) binary not null,
	primary key (UserName)
);

/*Create LoRa Request Node table*/
create table if not exists LRNode(
	LoRaId varchar(10) binary not null,
	RPackage varchar(200) binary not null,
	primary key (LoRaId)
);

/*Create LoRa Accept Node table*/
create table if not exists LANode(
	RPackage varchar(200) binary not null,
	primary key (RPackage)
);

/*Create LoRa Command Node table*/
create table if not exists LCNode(
	LoRaId varchar(10) binary not null,
	Command varchar(20) binary not null,
	primary key (LoRaId)
);

/*create LoRa Table Register table*/
create table if not exists LTRegister(
	TName varchar(20) binary not null,
	Property varchar(100) binary,
	primary key (TName)
);

/*Insert Init data*/
insert into LUser values('Administrator','administrator',1);
insert into LTRegister values('LNode','{"title":"Power Dissipation","datatype":"spline","data":["$time(1000)","LoRaPD"],"series":"LoRaId"}');