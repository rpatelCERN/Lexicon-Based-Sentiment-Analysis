CREATE Table substanceabuse(
index int,
tweetid bigint,
user_id bigint,
username varchar,
tweet text,
likes_count int,
hashtags varchar
);

CREATE Table sexual(
index int,
tweetid bigint,
user_id bigint,
username varchar,
tweet text,
likes_count int,
hashtags varchar
);

CREATE Table ptsd(
index int,
tweetid bigint,
user_id bigint,
username varchar,
tweet text,
likes_count int,
hashtags varchar
);

CREATE Table depression(
index int,
tweetid bigint,
user_id bigint,
username varchar,
tweet text,
likes_count int,
hashtags varchar
);

CREATE Table anxiety(
index int,
tweetid bigint,
user_id bigint,
username varchar,
tweet text,
likes_count int,
hashtags varchar
);

CREATE Table VA(
index int,
tweetid bigint,
user_id bigint,
username varchar,
tweet text,
likes_count int,
hashtags varchar
);

COPY ptsd FROM 
'/Users/rishipatel/ProjectStorage/NeuroFlow/twint/ptsdFormatted.csv'
DELIMITER ','
CSV HEADER;

COPY depression FROM 
'/Users/rishipatel/ProjectStorage/NeuroFlow/twint/depressionFormatted.csv'
DELIMITER ','
CSV HEADER;

COPY substanceabuse FROM 
'/Users/rishipatel/ProjectStorage/NeuroFlow/twint/substanceFormatted.csv'
DELIMITER ','
CSV HEADER;


COPY anxiety FROM 
'/Users/rishipatel/ProjectStorage/NeuroFlow/twint/anxietyFormatted.csv'
DELIMITER ','
CSV HEADER;

COPY sexual FROM 
'/Users/rishipatel/ProjectStorage/NeuroFlow/twint/sexualFormatted.csv'
DELIMITER ','
CSV HEADER;

COPY va FROM 
'/Users/rishipatel/ProjectStorage/NeuroFlow/twint/VAFormatted.csv'
DELIMITER ','
CSV HEADER;
CREATE TABLE AllTweets AS
((SELECT DISTINCT ON (tweetid) * FROM ptsd 
 UNION SELECT DISTINCT ON (tweetid) * FROM anxiety)  
 UNION (SELECT DISTINCT ON (tweetid) * FROM depression)
); 
INSERT INTO AllTweets (SELECT DISTINCT ON (tweetid) * FROM substanceabuse );
INSERT INTO AllTweets  (SELECT DISTINCT ON (tweetid) * FROM sexual );
INSERT INTO AllTweets  (SELECT DISTINCT ON (tweetid) *  FROM va );

SELECT COUNT(tweetid) FROM (SELECT DISTINCT ON (tweetid) * FROM AllTweets) AS distinctTweets
WHERE tweet LIKE '%Nam%' OR tweet LIKE '%Vietnam%' OR
tweet LIKE '%WWII%' OR tweet LIKE '%Korea%' OR tweet LIKE '%Iraq%' OR tweet LIKE '%Afghan%';

SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%Nam%' OR tweet LIKE '%Vietnam%';
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%WWII%';
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%Korea%';
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%Iraq%';
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%Afghan%';
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%Desert Storm%' OR tweet LIKE '%Gulf%';

SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%alcohol%'
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%drug%'
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%incarceration%' OR tweet LIKE '%prison%' OR tweet LIKE '%jail%'
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%homeless%'
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%harm%'

SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%bad back%'
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%hearing%' OR  tweet LIKE '%tinnitus%'
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%knee%'
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%medication%'
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%TBI%'
SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE tweet LIKE '%racism%'


SELECT DISTINCT ON (tweetid) * FROM AllTweets WHERE hashtags NOT LIKE '[]'
SELECT user_id,COUNT(user_id) FROM AllTweets GROUP BY user_id HAVING COUNT(user_id)>2 ORDER BY COUNT(user_id) DESC
SELECT user_id,COUNT(user_id),tweet FROM AllTweets GROUP BY user_id HAVING COUNT(user_id)>2 WHERE ORDER BY COUNT(user_id) DESC
SELECT user_id,COUNT(user_id) FROM AllTweets  WHERE tweet LIKE '%sleep%' GROUP BY user_id ORDER BY COUNT(user_id) DESC

SELECT username,tweet FROM AllTweets WHERE user_id=925416142318874624

