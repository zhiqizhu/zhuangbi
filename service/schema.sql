drop table if exists t_user;
create table t_user (
  id integer primary key autoincrement,
  user_name text not null,
  pass_word text not null,
  mail text not null
);