create table notebook
(
    id       integer primary key autoincrement,
    language varchar(20)    not null,
    class    varchar(20)    not null,
    title    varchar(200)   not null,
    describe varchar(10000) not null default '',
    code     varchar(50000) not null,
    useful   integer        not null default 0,
    utctime  integer        not null,
    extra    varchar(5000)
);