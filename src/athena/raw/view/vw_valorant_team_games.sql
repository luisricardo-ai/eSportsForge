CREATE OR REPLACE VIEW vw_valorant_team_games AS
    WITH cte_team1 AS (
        SELECT
            DISTINCT content.team1 AS team
        FROM raw.valorant_match_resume AS dataset
        CROSS JOIN UNNEST(result) AS t(content)
    ), cte_team2 AS (
        SELECT
            DISTINCT content.team2 AS team
        FROM raw.valorant_match_resume AS dataset
        CROSS JOIN UNNEST(result) AS t(content)
    ), cte_teams AS (
        SELECT * FROM cte_team1
        UNION ALL
        SELECT * FROM cte_team2
    )
    SELECT 
        team
        ,count(*) AS games_played
    FROM cte_teams
    GROUP BY
        team;