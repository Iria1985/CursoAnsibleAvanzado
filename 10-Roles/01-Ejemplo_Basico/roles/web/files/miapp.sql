
drop table if exists usuarios;

create table usuarios (
  id int auto_increment primary key not null,
  login varchar(50) not null unique,
  password varchar(100) not null);

insert into usuarios values (1,'perico','palotes');
insert into usuarios values (2,'fulanito','secreto');
insert into usuarios values (3,'menganito','abretesesamo');

