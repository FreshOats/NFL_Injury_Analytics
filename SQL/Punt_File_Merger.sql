DROP TABLE IF EXISTS punt_analytics;


CREATE TABLE punt_analytics AS
SELECT ppr.gamekey,
	ppr.playid,
	ppr.gsisid,
	pi.season_year,
	pi.season_type,
	pi.quarter,
	pi.score_home_visiting,
	gms.stadiumtype,
	gms.turf,
	gms.week,
	pp.p_position,
	r.player_activity,
	r.turnover_related,
	r.impact_type
FROM play_player_role AS ppr
INNER JOIN play_info AS pi ON (ppr.gamekey = pi.gamekey
																															AND ppr.playid = pi.playid)
INNER JOIN game_data AS gms ON (ppr.gamekey = gms.gamekey)
INNER JOIN player_punt_data AS pp ON (ppr.gsisid = pp.gsisid)
LEFT JOIN review as r ON (ppr.gamekey = r.gamekey
																										AND ppr.playid = r.playid
																										AND ppr.gsisid = r.gsisid);


DROP TABLE IF EXISTS concussion_ngs;


CREATE TABLE concussion_ngs AS
SELECT pa.gamekey,
	pa.playid,
	pa.gsisid,
	pa.season_year,
	pa.season_type,
	pa.quarter,
	pa.score_home_visiting,
	pa.stadiumtype,
	pa.turf,
	pa.week,
	pa.p_position,
	pa.player_activity,
	pa.turnover_related,
	pa.impact_type,
	ngs.g_time,
	ngs.x,
	ngs.y,
	ngs.o,
	ngs.dir
FROM punt_analytics as pa
INNER JOIN ngs ON (ngs.gsisid = pa.gsisid
																			AND ngs.playid = pa.playid
																			and ngs.gamekey = pa.gamekey)
WHERE pa.player_activity IS NOT NULL ;


