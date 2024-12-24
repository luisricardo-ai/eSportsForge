CREATE OR REPLACE VIEW raw.vw_valorant_match_resume AS
SELECT
    dt,
    split_part(content.match_page, '/', 2) AS match_id,
    content.match_page,
    content.team1,
    content.team2,
    content.score1,
    content.score2,
    content.tournament_name,
    content.round_info
FROM raw.valorant_match_resume AS dataset
CROSS JOIN UNNEST(result) AS t(content);