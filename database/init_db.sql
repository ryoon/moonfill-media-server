create table if not exists movies
(
  filepath text,
  filename text not null,
  normalizedFilepath text not null,
  dir text,
  suffix text not null,

  primary key(filepath)
);

create table if not exists users
(
  userid text,
  name text not null,
  validafter timestamp not null,
  validbefore timestamp not null,

  primary key(userid)
);

create table if not exists watchhistory
(
  filepath text not null,
  userid text not null,
  lastseen timestamp not null,
  progress integer not null,

  primary key(filepath, userid)
);

create table if not exists searchhistory
(
  userid text not null,
  keywords text not null,
  whensearched timestamp not null
);

insert into users values ('youko', '葉子', datetime('2022-07-23'), datetime('9999-12-31'));
insert into users values ('akiko', '明子', datetime('2022-07-23'), datetime('9999-12-31'));
insert into users values ('tomoko', '朋子', datetime('2022-07-23'), datetime('9999-12-31'));
insert into users values ('ryo', '龍', datetime('2022-07-23'), datetime('9999-12-31'));
