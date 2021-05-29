# 2.a
select i.pid, i.player, n.vid, n.village, n.population
from igralec i
         inner join naselje n on i.pid = n.pid
where n.population = (select max(population) from naselje);

# 2.b
select a.aid, a.alliance
from aliansa a
         right join igralec i on a.aid = i.aid
group by a.aid
having count(i.pid) = 60;

# 2.c
select count(i.pid)
from igralec i
         left join naselje n on i.pid = n.pid
where n.population > (select avg(population) from naselje);

# 2.d
select n.*
from igralec i
         inner join naselje n on i.pid = n.pid
where i.aid is null
order by x desc, y;

# 2.e
select p.tid, count(i.pid) as stevilo
from pleme p
         inner join igralec i on p.tid = i.tid
group by p.tid
order by stevilo desc
limit 1;

# 2.f
select a.aid, count(i.pid) as stevilo
from aliansa a
         inner join igralec i on a.aid = i.aid
group by a.aid
order by stevilo desc
limit 1;

# 2.g
# population.py

# 2.h
select i.player
from igralec i
where (
          select count(*)
          from igralec ii
                   inner join naselje nn on ii.pid = nn.pid
          where nn.x > 150
            and nn.x < 200
            and nn.y > 0
            and nn.y < 100
            and ii.pid = i.pid
      ) = 0;

# 2.i
# TODO: figure out a way to write this query
select count(*)
from aliansa a
         inner join igralec i on a.aid = i.aid
         inner join naselje n on i.pid = n.pid
where n.vid = 100;

#  2.j
# TODO: should I use mysql functions / whatever ?
select *
from igralec i
         inner join naselje n on i.pid = n.pid
where i.player = 'Sirena'
order by n.population desc;


# 3.a
start transaction;
# ustvarimo novo alianso, izmislimo si nov aid (123)
insert into aliansa (aid, alliance)
values (123, 'HORDA-CAR');
# ustrezno posodobimo fk zahtevanih igralcev
update igralec i
set i.aid = 123
WHERE i.aid IN (
    select a.aid
    from aliansa a
    where a.alliance = 'HORDA'
       or a.alliance = 'CAR'
);
commit;

# 3.b
delimiter //
CREATE TRIGGER before_player_insert
    BEFORE INSERT
    ON igralec
    FOR EACH ROW
BEGIN
    DECLARE player_count INTEGER;
    SET player_count = (
        select count(i.pid) as n
        from aliansa a
                 inner join igralec i on a.aid = i.aid
        WHERE a.aid = NEW.aid
        group by a.aid
    );
    IF player_count >= 60 THEN
        SIGNAL SQLSTATE '45000' SET message_text = 'Player count is limited to max 60 per alliance.';
    END IF;
end //
delimiter ;
# preverimo delovanje z spodnjim insertom (mora vrniti napako)
select count(*)
from aliansa a
where a.aid = 27;
INSERT INTO igralec (pid, player, tid, aid)
VALUES (123, 'Test igralec', 7, 27);